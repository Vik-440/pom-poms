import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
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
  constructor(private _poshaService: NovaPoshtaService, public _activeModal: NgbActiveModal, private _fb: FormBuilder) {}
  ngOnInit(): void {
    this.initForms();
    this.getRefs();
    if(!JSON.parse(localStorage.getItem('Sender'))) {
      this.getCitiesNps();
    } else {
      this.dataSender.patchValue({
        ...JSON.parse(localStorage.getItem('Sender'))
      })
    }
  }

  initForms() {
    this.dataSender = this._fb.group({
      city: ['Київ', Validators.required],
      cityShow: ['Київ'],
      first_name_client: ['Дана', [Validators.required, Validators.minLength(2)]],
      cityRef: '',
      second_name_client: ['Довженко', [Validators.required, Validators.minLength(2)]],
      np_number: [142, Validators.required],
      npRef: '',
      npShow: '',
      phone: ['380991162803', [Validators.required]],
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
      phone: [this.data.phone_client, Validators.required],
    });
    this.dataParcel = this._fb.group({
      payerType: 'Sender',
      paymentMethod: 'NonCash',
      dateTime: [null, Validators.required],
      serviceType: ['WarehouseWarehouse', Validators.required],
      cargoType: ['Parcel', Validators.required],
      weight: [null, [Validators.required, Validators.min(0.1)]],
      cost: [null, Validators.required],
      description: ['Спортивні товари', Validators.required],
    });
  }

  getRefs() {
    this._poshaService.getCounterpartyRef('Sender');
    this._poshaService.getCounterpartyRef('Recipient');
  }

  getCitiesNps(form = this.dataSender, type = 'Sender') {
    this.isShowSpinner = true;
    console.log(form.value);
    this._poshaService
      .getCities(form.value.cityShow)
      .pipe(
        switchMap((cities: any) => {
          console.log(this.data, form.value.cityShow);
          this.itemCities = cities.data[0].Addresses;
          form.patchValue({
            cityRef: this.itemCities[0].Ref,
            city: this.itemCities[0].Present,
            cityShow: this.itemCities[0].MainDescription
          });
          return this._poshaService.getWarehouses(form.value.cityShow);
        })
      )
      .subscribe((data: any) => {
        this.itemNPs = data.data;
        this.selectedNP = this.itemNPs.findIndex((item) => +item.Number === +form.value.np_number);
        this.selectedNP = this.selectedNP === -1 ? 0 : this.selectedNP;
        console.log(data, this.itemNPs, this.selectedNP);
        form.patchValue({
          np_number: this.itemNPs[this.selectedNP].Number,
          npRef: this.itemNPs[this.selectedNP].Ref,
          npShow: this.itemNPs[this.selectedNP].Description
        });
        localStorage.setItem('Sender', JSON.stringify(this.dataSender.value) )
        console.log('form', form)
        this.isShowSpinner = false;
      });
  }

  changePage(action: string) {
    this.page = this.page + (action === '+' ? +1 : +'-1');
    if (this.page === 2) {
      this.getCitiesNps(this.dataRecipient);
    } else if (this.page === 1) {
      // this.getCitiesNps(this.dataSender);
    } else if (this.page === 3) {
      this.getAllInd();
    }
  }

  getAllInd() {
    const params = {
      first_name_client: this.dataRecipient.value.first_name_client,
      second_name_client: this.dataRecipient.value.second_name_client,
      phone: (this.dataRecipient.value.phone).replaceAll("-", ''),
    };
    this._poshaService.getIdentifikator(params);
  }

  changeCity(value, who) {
    this.isShowSpinner = true;
    const form = who === 'sender' ? this.dataSender : this.dataRecipient;
    console.log( this.itemCities[value])
    form.patchValue({
      cityRef: value.selectedItems[0].value.Ref,
      city: value.selectedItems[0].value.Present,
      cityShow: value.selectedItems[0].value.MainDescription
    });
    console.log(this.dataSender.value)
    this._poshaService.getWarehouses(form.value.cityShow).subscribe((data: any) => {
      this.itemNPs = data.data;
      console.log(data, this.itemNPs)
      this.selectedNP = this.itemNPs.findIndex((item) => +item.Number === +form.value.np_number);
      this.selectedNP = this.selectedNP === -1 ? 0 : this.selectedNP;
      console.log(this.selectedNP, this.itemNPs)
      if(this.itemNPs.length) {
        form.patchValue({
          np_number: this.itemNPs[this.selectedNP].Number,
          npRef: this.itemNPs[this.selectedNP].Ref,
          npShow: this.itemNPs[this.selectedNP].Description
        });
      }
      this.isShowSpinner = false;
    });
  }

  changeNP(value, who) {
    const form = who === 'sender' ? this.dataSender : this.dataRecipient;
    console.log(this.itemNPs[value], value)
    form.patchValue({
      np_number: value.selectedItems[0].value.Number,
      npRef: value.selectedItems[0].value.Ref,
      npShow: value.selectedItems[0].value.Description
    });
    console.log(form)
  }

  createInternetDocument() {
    const paramsForDoc = {
      PayerType: this.dataParcel.value.payerType,
      PaymentMethod: this.dataParcel.value.paymentMethod,
      DateTime: this.editData(this.dataParcel.value.dateTime),
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
    };

    this._poshaService.createInternetDocument(paramsForDoc).subscribe((data: any) => {
      if(data.success) {
        this.pdfSrc = `https://my.novaposhta.ua/orders/printMarking85x85/orders[]/${data.data[0].Ref}/type/pdf/apiKey/${this._poshaService.apiKey}`;
        window.open(this.pdfSrc, "_blank");
        this.closeModal();
      } else {
        this.showAlertError();
      }
    });
  }

  editData(data) {
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

  showAlertError() {
    this.alert = {
      isShow: true,
      type: 'danger',
      message: 'Уппс, щось пішло не так',
    };
    setTimeout(() => {
      this.alertChange(false);
    }, 3000);
  }

  alertChange(e) {
    this.alert.isShow = e;
  }

  closeModal() {
    this._activeModal.close();
  }
}
