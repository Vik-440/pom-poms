import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup, UntypedFormBuilder, Validators } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { debounceTime, filter, from, switchMap } from 'rxjs';
import { NovaPoshtaService } from '../services/poshta.service';
@Component({
  selector: 'app-nove-poshta-modal',
  templateUrl: './nove-poshta-modal.component.html',
  styleUrls: ['./nove-poshta-modal.component.sass'],
})
export class NovePoshtaModalComponent implements OnInit {
  @Input() data;
  @Output() closeModalNP = new EventEmitter();

  dataSender: FormGroup;
  dataRecipient: FormGroup;
  dataParcel: FormGroup;
  itemCities: any[];
  itemNPs: any[];
  page: number = 1;
  selectedNP: number = 0;
  isShowSpinner: boolean = false;
  todayDay = {
    year: new Date().getFullYear(),
    day: new Date().getDate(),
    month: new Date().getMonth() + 1,
  };
  alert = {
    type: '',
    message: '',
    isShow: false,
  };
  pdfSrc: string;
  isPackaging: boolean = false;
  packList = [];
  modalContentEl = document.querySelector('.modal-content');
  modalDialog = document.querySelector('.modal-dialog');
  constructor(private _poshaService: NovaPoshtaService, public _activeModal: NgbActiveModal, private _fb: UntypedFormBuilder) { }
  ngOnInit(): void {
    this.initForms();
    this.getRefs();
    this.modalContentEl = document.querySelector('.modal-content');
    this.modalDialog = document.querySelector('.modal-dialog');
    if (!JSON.parse(localStorage.getItem('Sender'))) {
      this.getCitiesNps();
    } else {
      this.dataSender.patchValue({
        ...JSON.parse(localStorage.getItem('Sender')),
      });
    }
  }

  initForms() {
    this.dataSender = this._fb.group({
      city: ['Київ', Validators.required],
      cityShow: ['Київ'],
      first_name_client: ['', [Validators.required, Validators.minLength(2)]],
      cityRef: '',
      second_name_client: ['', [Validators.required, Validators.minLength(2)]],
      np_number: [142, Validators.required],
      npRef: '',
      npShow: '',
      phone: ['', [Validators.required]],
      categoryOfWarehouse: '',
    });
    this.dataRecipient = this._fb.group({
      city: [this.data.sity, Validators.required],
      cityShow: this.data.sity,
      cityRef: '',
      first_name_client: [this.data.first_name_client, [Validators.required, Validators.minLength(2)]],
      second_name_client: [this.data.second_name_client, [Validators.required, Validators.minLength(2)]],
      np_number: [this.data.np_number, Validators.required],
      npShow: '',
      npRef: '',
      phone: [this.data.phone_recipient, Validators.required],
      categoryOfWarehouse: '',
    });
    this.dataParcel = this._fb.group({
      payerType: 'Recipient',
      paymentMethod: 'Cash',
      dateTime: [{ 
        year: new Date().getFullYear(),
        month: +String(new Date().getMonth() + 1).padStart(2, '0'),
        day: +String(new Date().getDate()).padStart(2, '0'), 
      }, Validators.required],
      serviceType: ['WarehouseWarehouse', Validators.required],
      cargoType: ['Parcel', Validators.required],
      weight: [1, [Validators.required, Validators.min(0.1)]],
      cost: [this.data.sum_payment, Validators.required],
      description: ['Спортивні товари', Validators.required],
      packing: [''],
      volumetricHeight: [1],
      volumetricLength: [1],
      volumetricWidth: [1],
    });
  }

  getRefs() {
    this._poshaService.getCounterpartyRef('Sender');
    this._poshaService.getCounterpartyRef('Recipient');
  }

  getCitiesNps(form = this.dataSender) {
    this.isShowSpinner = true;
    this._poshaService
      .getCities(form.value.cityShow)
      .pipe(
        switchMap((cities: any) => {
          this.itemCities = cities.data[0].Addresses;
          if(this.itemCities[0]) {
            form.patchValue({
              cityRef: this.itemCities[0].Ref,
              city: this.itemCities[0].Present,
              cityShow: this.itemCities[0].MainDescription,
            });
          }
          return this._poshaService.getWarehouses(form.value.cityShow);
        })
      )
      .subscribe((data: any) => {
        this.itemNPs = data.data;

        this.selectedNP = this.itemNPs.findIndex((item) => +item.Number === +form.value.np_number);
        this.selectedNP = this.selectedNP === -1 ? 0 : this.selectedNP;
        form.patchValue({
          np_number: this.itemNPs[this.selectedNP]?.Number,
          npRef: this.itemNPs[this.selectedNP]?.Ref,
          npShow: this.itemNPs[this.selectedNP]?.Description,
          categoryOfWarehouse: this.itemNPs[this.selectedNP]?.CategoryOfWarehouse,
        });
        localStorage.setItem('Sender', JSON.stringify(this.dataSender.value));
        this.isShowSpinner = false;
      });
  }

  changePage(action: string) {
    this.page = this.page + (action === '+' ? +1 : +'-1');
    if (this.page === 2) {
      this.getCitiesNps(this.dataRecipient);
    } else if (this.page === 3) {
      this.dataParcel.patchValue({
        serviceType: this.dataRecipient.value.categoryOfWarehouse === 'Postomat' ? 'WarehousePostomat' : 'WarehouseWarehouse',
      })
      this.getAllInd();
    }
  }

  getAllInd() {
    const params = {
      first_name_client: this.dataRecipient.value.first_name_client,
      second_name_client: this.dataRecipient.value.second_name_client,
      phone: this.dataRecipient.value.phone.replaceAll('-', ''),
    };
    this._poshaService.getIdentifikator(params);
  }

  changeCity(value, who) {
    this.isShowSpinner = true;
    const form = who === 'sender' ? this.dataSender : this.dataRecipient;
    form.patchValue({
      cityRef: value.selectedItems[0].value.Ref,
      city: value.selectedItems[0].value.Present,
      cityShow: value.selectedItems[0].value.MainDescription,
    });
    this._poshaService.getWarehouses(form.value.cityShow).subscribe((data: any) => {
      this.itemNPs = data.data;
      this.selectedNP = this.itemNPs.findIndex((item) => +item.Number === +form.value.np_number);
      this.selectedNP = this.selectedNP === -1 ? 0 : this.selectedNP;
      if (this.itemNPs.length) {
        form.patchValue({
          np_number: this.itemNPs[this.selectedNP].Number,
          npRef: this.itemNPs[this.selectedNP].Ref,
          npShow: this.itemNPs[this.selectedNP].Description,
          categoryOfWarehouse: this.itemNPs[this.selectedNP]?.CategoryOfWarehouse,
        });
      }
      this.isShowSpinner = false;
    });
  }

  changeNP(value, who) {
    const form = who === 'sender' ? this.dataSender : this.dataRecipient;
    form.patchValue({
      np_number: value.selectedItems[0].value.Number,
      npRef: value.selectedItems[0].value.Ref,
      npShow: value.selectedItems[0].value.Description,
      categoryOfWarehouse: value.selectedItems[0].value.CategoryOfWarehouse,
    });
  }

  cloneData() {
    this.page = 3;
    this.modalContentEl.classList.remove('small');
    this.modalDialog.classList.remove('small');
  }

  createInternetDocument() {
    let paramsForDoc = {
      PayerType: this.dataParcel.value.payerType,
      PaymentMethod: this.dataParcel.value.paymentMethod,
      DateTime: this.editDate(this.dataParcel.value.dateTime),
      CargoType: this.dataParcel.value.cargoType,
      Weight: this.dataParcel.value.weight,
      ServiceType: this.dataParcel.value.serviceType,
      SeatsAmount: 1,
      Description: this.dataParcel.value.description,
      Cost: this.dataParcel.value.cost,
      CitySender: this.dataSender.value.cityRef,
      SendersPhone: this.dataSender.value.phone,
      CityRecipient: this.dataRecipient.value.cityRef,
      RecipientsPhone: this.dataRecipient.value.phone,
      SenderAddress: this.dataSender.value.npRef,
      RecipientAddress: this.dataRecipient.value.npRef,
      OptionsSeat: null,
    };

    if (this.isPackaging) {
      paramsForDoc = {
        ...paramsForDoc,
        OptionsSeat: [
          {
            packRef: this.dataParcel.value.packing,
            volumetricWidth: this.dataParcel.value.volumetricWidth,
            volumetricLength: this.dataParcel.value.volumetricLength,
            volumetricHeight: this.dataParcel.value.volumetricHeight,
            weight: this.dataParcel.value.weight,
          },
        ],
      };
    }

    this._poshaService.createInternetDocument(paramsForDoc).subscribe((data: any) => {
      if (data.success) {
        this.pdfSrc = 
          `https://my.novaposhta.ua/orders/printMarking85x85/orders[]/${data.data[0].Ref}/type/pdf/apiKey/${this._poshaService.apiKey}`;
        window.open(this.pdfSrc, '_blank');
        this.page = 4;
        this.modalContentEl.classList.add('small');
        this.modalDialog.classList.add('small');
      } else {
        const errors = data.errors.join(`\n`);
        console.log(errors)
        this.showAlertError(errors);
      }
    });
  }

  editDate(data) {
    const month = +data.month < 10 ? '0' + data.month : data.month;
    const day = +data.day < 10 ? '0' + data.day : data.day;
    return data ? [day, month, data.year].join('.') : null;
  }

  searchCity(query) {
    from([1, 2, 3, 4, 5])
      .pipe(
        debounceTime(2000),
        filter(() => query.term.length > 3),
        switchMap(() => this._poshaService.getCities(query.term))
      )
      .subscribe((data: any) => {
        this.itemCities = data.data[0].Addresses;
      });
  }

  changePack() {
    if (this.isPackaging) {
      ['packing', 'volumetricWidth', 'volumetricLength', 'volumetricHeight'].forEach((control) =>
        this.dataParcel.get(control).setValidators([Validators.required])
      );
    } else {
      ['packing', 'volumetricWidth', 'volumetricLength', 'volumetricHeight'].forEach((control) =>
        this.dataParcel.get(control).setValidators(null)
      );
    }
    this.dataParcel.get('packing').updateValueAndValidity();
    if (this.isPackaging && !this.packList.length) {
      this._poshaService.getPackList().subscribe((data: any) => {
        this.packList = data.data;
      });
    }
  }

  showAlertError(message = null) {
    this.alert = {
      isShow: true,
      type: 'danger',
      message: message || 'Уппс, щось пішло не так',
    };
    setTimeout(() => {
      this.alertChange(false);
    }, 3000);
  }

  alertChange(e) {
    this.alert.isShow = e;
  }

  closeModal(value) {
    this._activeModal.close();
    this.closeModalNP.emit(value)
  }
}
