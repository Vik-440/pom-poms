import { Component, Input, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';
import locale from 'date-fns/locale/en-US';
import * as moment from 'moment';
import { DatepickerOptions } from 'ng2-datepicker';
import { NgxSpinnerService } from 'ngx-spinner';
import { filter, tap } from 'rxjs';
import { CreateOrderService } from '../services/create-order.service';

@Component({
  selector: 'app-create-order',
  templateUrl: './create-order.component.html',
  styleUrls: ['./create-order.component.sass']
})
export class CreateOrderComponent implements OnInit {

  constructor(private fb: FormBuilder, private service: CreateOrderService, private spinner: NgxSpinnerService) { }

  @Input() isNew: Boolean = true;
  orderForm: FormArray;
  clientForm: FormGroup;
  isGetPostR: Boolean = false;
  recipientForm: FormGroup;
  priceAll: FormGroup;
  idOrder: number = 0;
  isSaveClient: Boolean = false;
  isSaveRecipient: Boolean;
  fulfilledOrder: Boolean = false;
  options: DatepickerOptions = {
    minDate: new Date(''),
    format: 'yyyy-MM-dd',
    formatDays: 'EEEEE',
    firstCalendarDay: 1,
    locale: locale,
    position: 'bottom',
    placeholder: 'dd.mm.yyyy',
    calendarClass: 'datepicker-default',
    scrollBarColor: '#dfe3e9'
  };

  orders = [1]

  dateToday = new Date();
  dataPlaneOrder = null;
  dataSendOrder = null;
  dateForms: FormGroup;
  isRecipient = false;
  kodItems;
  materialsItems;
  clientDataItems;
  infoForSave: any;
  commentOrder: string = '';
  discount: number = 0;
  doneOrder: Boolean = false;

  ngOnInit(): void {
    this.dateForms = this.fb.group({
      data_order: moment().format('YYYY-MM-DD'),
      data_plane_order: null,
      data_send_order: null
    })
    
    this.priceAll = this.fb.group({
      sum_payment: 0,
      real_money: 0,
      different: 0
    });

    this.orderForm =  
      this.fb.array([
        this.fb.group({
          kod_model: null,
          id_model: null,
          kolor_model: null,
          id_color_1: null,
          name_color_1: null,
          id_color_part_1: null,
          id_color_2: null,
          name_color_2: null,
          id_color_part_2: null,
          id_color_3: null,
          name_color_3: null,
          id_color_part_3: null,
          id_color_4: null,
          name_color_4: null,
          id_color_part_4: null,
          price_model: null,
          quantity_pars_model: null,
          sum_pars: null,
          comment_model: null,
          isNew: true,
          isChange: false
        })
      ]);

    this.clientForm = this.fb.group({
      id_client: null,
      phone_client: null,
      second_name_client: null,
      first_name_client: null,
      surname_client: null,
      sity: null,
      np_number: null,
      name_team: null,
      coach: null,
      zip_code: null,
      street_house_apartment: null,
      comment_client: null
    });

    this.recipientForm = this.fb.group({
      id_client: null,
      coach: null,
      phone_client: null,
      second_name_client: null,
      first_name_client: null,
      surname_client: null,
      sity: null,
      np_number: null,
      name_team: null,
      zip_code: null,
      street_house_apartment: null,
      comment_client: null,
    });

    this.viewChanges();
  }

  sumAll() {
    const sumAllItems = [];
    this.priceAll.patchValue({
      sum_payment: 0
    })
    this.orderForm.controls.map(order => {
      this.priceAll.patchValue({
        sum_payment: this.priceAll.value.sum_payment + order.value.sum_pars
      })
    });   
    sumAllItems.push(this.priceAll.value.sum_payment, this.priceAll.value.real_money, this.priceAll.value.different);
    return sumAllItems.join(' / ')
  }

  viewChanges() {
    this.orderForm.controls.map((order, index) => {
      order.get('quantity_pars_model').valueChanges.pipe(
        tap(data => {
          order.patchValue({
            sum_pars: data * order.value.price_model
          })
        })
      ).subscribe()

      order.get('price_model').valueChanges.pipe(
        tap(data => {
          order.patchValue({
            sum_pars: data * order.value.quantity_pars_model
          })
        })
      ).subscribe()

      order.get('kolor_model').valueChanges.subscribe(() => {
        order.patchValue({
          isNew: true
        })
      })

      order.get('id_color_part_1').valueChanges.subscribe(() => {
        order.patchValue({
          isNew: true
        })
      })

      order.get('id_color_part_2').valueChanges.subscribe(() => {
        order.patchValue({
          isNew: true
        })
      })

      order.get('id_color_part_3').valueChanges.subscribe(() => {
        order.patchValue({
          isNew: true
        })
      })

      order.get('id_color_part_4').valueChanges.subscribe(() => {
        order.patchValue({
          isNew: true
        })
      })
    });

    this.recipientForm.valueChanges.subscribe(() => {
      if(this.isSaveRecipient) {
        this.isSaveRecipient = false;
      }
    });

    this.clientForm.valueChanges.subscribe(() => {
      if(this.isSaveClient) {
        this.isSaveClient = false;
      }
    })
  }

  changeKodModel(value, index) {
    if(value.length >= 3) {
      this.service.getInfoForOrder({ur_kod: value}).subscribe((kods: any) => {
        this.kodItems = kods?.kod_model;
      })
    }
  }

  changeMaterial(value, index) {
    if(value.length >= 3) {
      this.service.getInfoForOrder({ur_kolor: value}).subscribe((materials: any) => {
        this.materialsItems = materials;
      })
    }
  }

  chooseKode(value, index) { 
    if(!this.kodItems) {
      this.orderForm.controls.map((order, ind) => {
        if(ind === index && value) {
          order.patchValue({
            kod_model: value,
          })
        } else if(!value){
          order.patchValue({
            kod_model: null
          })
        }
        return;
      })
    }
     if(this.kodItems?.includes(value)) {
      this.orderForm.controls.map((order, ind) => {
        this.service.getInfoForOrder({ sl_kod: value }).subscribe((data: any) => {
          if(index === ind && Object.keys(data).length){
            order.patchValue({
              id_model: data.id_model,
              kod_model: data.kod_model,
              kolor_model: data.kolor_model,
              name_color_1: data.name_color_1 || null,
              id_color_part_1: data.id_color_part_1,
              id_color_1: data.id_color_1,
              id_color_2: data.id_color_2,
              id_color_3: data.id_color_3,
              id_color_4: data.id_color_4,
              name_color_2: data.name_color_2 || null,
              id_color_part_2: data.id_color_part_2,
              name_color_3: data.name_color_3 || null,
              id_color_part_3: data.id_color_part_3,
              name_color_4: data.name_color_4 || null,
              id_color_part_4: data.id_color_part_4,
              price_model: data.price_model,
              comment_model: data.comment_model,
              isNew: false,
              isChange: false
            }, {emitEvent: false})

           console.log(order);
            
          }
        })
      })
    }
    this.kodItems = [];
  }

  resetMaterialsItems() {
    this.materialsItems = [];
  }

  changeCoach(form, field) {
    if(form.value[field] === form.value.second_name_client) {
      form.patchValue({
        [field]: null
      });
    } else {
      form.patchValue({
        [field]: form.value.second_name_client
      });
    }
  }
  addOrder() {
    this.orderForm.push(this.fb.group({
      kod_model: null,
      id_model: null,
      kolor_model: null,
      id_color_1: null,
      name_color_1: null,
      name_color_2: null,
      name_color_3: null,
      name_color_4: null,
      id_color_part_1: null,
      id_color_2: null,
      id_color_part_2: null,
      id_color_3: null,
      id_color_part_3: null,
      id_color_4: null,
      id_color_part_4: null,
      price_model: null,
      quantity_pars_model: null,
      sum_pars: null,
      comment_model: null,
      isNew: true,
      isChange: false
    }));
    this.viewChanges();
  }

  deleteOrder(index) {
    this.orderForm.controls.splice(index, 1);
  }

  saveOrder(index, order) {
    const params = {
      "sl_id_model": order.value.id_model || 0,
      "kod_model": order.value.kod_model || 0,
      "id_color_1": order.value.id_color_1 || 0,
      "id_color_part_1": +order.value.id_color_part_1 || 0,
      "id_color_2" :  +order.value.id_color_2 || 0,
      "id_color_part_2" : +order.value.id_color_part_2 || 0,
      "id_color_3" :  +order.value.id_color_3 || 0,
      "id_color_part_3" : +order.value.id_color_part_3 || 0,
      "id_color_4" :  +order.value.id_color_4  || 0,
      "id_color_part_4" : +order.value.id_color_part_4  || 0,
      "price_model":  order.value.price_model  || 0,
      "comment_model":  order.value.comment_model  || 0,
      "kolor_model":  order.value.kolor_model || 0
    }

    this.service.getInfoForOrder(params).subscribe(() => {
      order.patchValue({
        isNew: false
      })
    });
  }

  changeClientInfo(phone, minLength, keySend) {
    if(phone.length >= minLength) {
      this.service.getInfoForOrder({ [keySend] : phone}).subscribe((phones: any) => {
        this.clientDataItems = Object.values(phones)[0];
      })
    }
  }

  selectedItemClient(value, keySend, form = this.clientForm, saveBtn = 'isSaveClient'){
    if(value && this.clientDataItems.includes(value)) {
      this.service.getInfoForOrder({ [keySend]: value })
      .pipe(filter(() => value))
      .subscribe((dataClient: any) => {
        form.setValue({
          coach: dataClient?.coach,
          comment_client: dataClient.comment_client,
          first_name_client: dataClient.first_name_client,
          id_client: dataClient.id_client,
          name_team: dataClient.name_team,
          phone_client: dataClient.phone_client,
          second_name_client: dataClient.second_name_client,
          sity: dataClient.sity,
          street_house_apartment: dataClient.street_house_apartment,
          surname_client: dataClient.surname_client,
          zip_code: dataClient.zip_code,
          np_number: dataClient.np_number
        }, {emitEvent: false});
        this[saveBtn] = true;
      })
    }
    this.clientDataItems = [];
  }

  saveClient() {
    const params = {
      "sl_id_recipient": null,
      "phone_client": this.clientForm.value.phone_client,
      "second_name_client": this.clientForm.value.second_name_client,
      "first_name_client": this.clientForm.value.first_name_client,
      "surname_client": this.clientForm.value.surname_client,
      "np_number": this.clientForm.value.np_number,
      "name_team": this.clientForm.value.name_team,
      "coach": this.clientForm.value.coach,
      "zip_code": this.clientForm.value.zip_code,
      "street_house_apartment": this.clientForm.value.street_house_apartment,
      "comment_client": this.clientForm.value.comment_client,
      "sity": this.clientForm.value.sity
    }

    this.service.getInfoForOrder(params).subscribe(data => {
      this.isSaveClient = true;
    })
  }

  saveRecipient() {
    const params = {
      "sl_id_recipient": null,
      "phone_client": this.recipientForm.value.phone_client,
      "second_name_client": this.recipientForm.value.second_name_client,
      "first_name_client": this.recipientForm.value.first_name_client,
      "surname_client": this.recipientForm.value.surname_client,
      "np_number": this.recipientForm.value.np_number,
      "id_team": this.recipientForm.value.id_team,
      "coach": this.clientForm.value.coach,
      "zip_code": this.recipientForm.value.zip_code,
      "street_house_apartment": this.recipientForm.value.street_house_apartment,
      "comment_client": this.recipientForm.value.comment_client,
      "sity": this.recipientForm.value.sity
    }

    this.service.getInfoForOrder(params).subscribe(() => {
      this.isSaveRecipient = true;
    });
  }

  makeArrayDataOrder(key) {
    const result = [];
    this.orderForm.value.map(order => {
      result.push(order[key])
    })
    return result;
  }

  saveAll() {
    const params = {
      id_order: this.idOrder,
      data_order: moment(this.dateToday).format('YYYY-MM-DD'),
      id_client: this.clientForm.value.id_client,
      id_recipient: !this.isRecipient ? this.clientForm.value.id_client : this.recipientForm.value.id_client, // (2 або ід_клієнт)
      id_model: this.makeArrayDataOrder('id_model'),
      quantity_pars_model: this.makeArrayDataOrder('quantity_pars_model'),
      data_plane_order: this.dataPlaneOrder ? moment(this.dataPlaneOrder).format('YYYY-MM-DD') : null, // - прогнозована
      data_send_order: this.dataSendOrder ? moment(this.dataSendOrder).format('YYYY-MM-DD') : null, //- бажана
      discont_order: this.discount,
      sum_payment: this.sumAll().split('/')[0].trim(),
      fulfilled_order: false,
      comment_order: this.commentOrder
    }

    this.service.saveOrder(params).subscribe((data: any) => {
      this.idOrder = data.id_order;
      this.doneOrder = true;
    });
  }

  getOrder(event) {
    const params = {
      edit_order: this.idOrder
    };
    this.service.getInfoForOrder(params).pipe(
      filter((data: any) => {
        if(!!!Object.keys(data).length) {
          this.commentOrder = '';
          this.dateToday = new Date();
          this.dataPlaneOrder = null;
          this.dataSendOrder = null;
          this.discount = null;
          this.fulfilledOrder = false;
          this.clientForm.reset();
          this.recipientForm.reset();
          this.orderForm.reset();
        }
        console.log(this.dataPlaneOrder);
        
        return !!Object.keys(data).length;
      }),
      tap(() => {
        this.spinner.show();
      })
    ).subscribe((data: any) => {
      console.log(data);
      this.commentOrder = data.comment_order;
      this.dateToday = new Date(data.data_order);
      this.dataPlaneOrder = new Date(data.data_plane_order);
      this.dataSendOrder = new Date(data.data_send_order);
      this.discount = data.discont_order;
      this.fulfilledOrder = data.fulfilled_order;
      this.service.getInfoForOrder({open_id_client: data.id_client})
        .subscribe((dataClient: any) => {
          this.clientForm.setValue({
            coach: dataClient?.coach,
            comment_client: dataClient.comment_client,
            first_name_client: dataClient.first_name_client,
            id_client: dataClient.id_client,
            name_team: dataClient.name_team,
            phone_client: dataClient.phone_client,
            second_name_client: dataClient.second_name_client,
            sity: dataClient.sity,
            street_house_apartment: dataClient.street_house_apartment,
            surname_client: dataClient.surname_client,
            zip_code: dataClient.zip_code,
            np_number: dataClient.np_number
          }, {emitEvent: false});
        });

        if(data.id_client !== data.id_recipient) {
          this.isRecipient = true;
          this.service.getInfoForOrder({id_recipient: data.id_recipient})
            .subscribe((dataRecipient: any) => {
              this.recipientForm.setValue({
                coach: dataRecipient?.coach,
                comment_client: dataRecipient.comment_client,
                first_name_client: dataRecipient.first_name_client,
                id_client: dataRecipient.id_client,
                name_team: dataRecipient.name_team,
                phone_client: dataRecipient.phone_client,
                second_name_client: dataRecipient.second_name_client,
                sity: dataRecipient.sity,
                street_house_apartment: dataRecipient.street_house_apartment,
                surname_client: dataRecipient.surname_client,
                zip_code: dataRecipient.zip_code,
                np_number: dataRecipient.np_number
              }, {emitEvent: false});
            })
        }

        data.id_model.forEach((model, index) => {
          this.service.getInfoForOrder({open_id_model: model}).subscribe((dataModel: any) => {
            this.orderForm.clear();
            this.orderForm.push(this.fb.group({
              id_model: dataModel.id_model,
              kod_model: dataModel.kod_model,
              kolor_model: dataModel.kolor_model,
              name_color_1: dataModel.name_color_1 || null,
              id_color_part_1: dataModel.id_color_part_1,
              id_color_1: dataModel.id_color_1,
              id_color_2: dataModel.id_color_2,
              id_color_3: dataModel.id_color_3,
              id_color_4: dataModel.id_color_4,
              name_color_2: dataModel.name_color_2 || null,
              id_color_part_2: dataModel.id_color_part_2,
              name_color_3: dataModel.name_color_3 || null,
              id_color_part_3: dataModel.id_color_part_3,
              name_color_4: dataModel.name_color_4 || null,
              id_color_part_4: dataModel.id_color_part_4,
              price_model: dataModel.price_model,
              comment_model: dataModel.comment_model,
              quantity_pars_model: data.quantity_pars_model[index],
              sum_pars: data.quantity_pars_model[index] *  dataModel.price_model,
              isNew: false,
              isChange: false
            }));
          })
        })
      this.priceAll.patchValue({
        sum_payment: data.sum_payment
      })
      this.spinner.hide();
      
    });
  }
}
