import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';
import locale from 'date-fns/locale/en-US';
import { DatepickerOptions } from 'ng2-datepicker';
import { filter, tap } from 'rxjs';
import { CreateOrderService } from '../services/create-order.service';

@Component({
  selector: 'app-create-order',
  templateUrl: './create-order.component.html',
  styleUrls: ['./create-order.component.sass']
})
export class CreateOrderComponent implements OnInit {

  constructor(private fb: FormBuilder, private service: CreateOrderService) { }

  orderForm: FormArray;
  clientForm: FormGroup;
  priceAll: FormGroup;
  options: DatepickerOptions = {
    minDate: new Date(''),
    format: 'dd.MM.yyyy',
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
  isRecipient = false;
  kodItems;
  materialsItems;
  clientDataItems;

  ngOnInit(): void {
    this.priceAll = this.fb.group({
      sum_payment: 0,
      real_money: 0,
      different: 0
    });
    this.orderForm =  
      this.fb.array([
        this.fb.group({
          kod_model: null,
          kolor_model: null,
          id_color_1: null,
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
      coach: false,
      zip_code: null,
      street_house_apartment: null,
      comment_client: null
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
    })
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
        this.materialsItems = materials?.name_color;
      })
    }
  }

  chooseKode(value, index) { 
    if(!this.kodItems) {
      this.orderForm.controls.map((order, ind) => {
        if(ind === index) {
          order.patchValue({
            kod_model: `id__ - ` + value,
          })
        }
        return;
      })
    }
     
    this.orderForm.controls.map((order, ind) => {
      this.service.getInfoForOrder({ sl_kod: value }).subscribe((data: any) => {
        if(index === ind && Object.keys(data).length){
          order.patchValue({
            kod_model: `id${data.id_model} - ` + data.kod_model,
            kolor_model: data.kolor_model,
            id_color_1: data.id_color_1,
            id_color_part_1: data.id_color_part_1,
            id_color_2: data.id_color_2,
            id_color_part_2: data.id_color_part_2,
            id_color_3: data.id_color_3,
            id_color_part_3: data.id_color_part_3,
            id_color_4: data.id_color_4,
            id_color_part_4: data.id_color_part_4,
            price_model: data.price_model,
            comment_model: data.comment_model,
            isNew: false,
            isChange: false
          })
        }
      })
      this.kodItems = [];
    })
  }

  resetMaterialsItems() {
    this.materialsItems = [];
  }

  addOrder() {
    this.orderForm.push(this.fb.group({
      kod_model: null,
      kolor_model: null,
      id_color_1: null,
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
      "sl_id_model": order.value.id_model,
      "kod_model": order.value.kod_model,
      "id_color_1": order.value.id_color_1,
      "id_color_part_1": order.value.id_color_part_1,
      "id_color_2" :  order.value.id_color_2,
      "id_color_part_2" : order.value.id_color_part_2,
      "id_color_3" :  order.value.id_color_3,
      "id_color_part_3" : order.value.id_color_part_3,
      "id_color_4" :  order.value.id_color_4,
      "id_color_part_4" : order.value.id_color_part_4,
      "price_model":  order.value.price_model,
      "comment_model":  order.value.comment_model,
      "kolor_model":  order.value.kolor_model
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

  selectedItemClient(value, keySend){
    this.clientDataItems = [];

    this.service.getInfoForOrder({ [keySend]: value })
    .pipe(filter(() => value))
    .subscribe((data: any) => {
      console.log(data);
      let dataClient = data[0]
      this.clientForm.patchValue({
        coach: dataClient.coach,
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
      })
    })
  }

  saveClient() {
    console.log(1);
    
    const params = {
      "sl_id_recipient": null,
      "phone_client": this.clientForm.value.phone_client,
      "second_name_client": this.clientForm.value.second_name_client,
      "first_name_client": this.clientForm.value.first_name_client,
      "surname_client": this.clientForm.value.surname_client,
      "id_sity": this.clientForm.value.id_sity,
      "np_number": this.clientForm.value.np_number,
      "id_team": this.clientForm.value.id_team,
      "coach": this.clientForm.value.coach,
      "zip_code": this.clientForm.value.zip_code,
      "street_house_apartment": this.clientForm.value.street_house_apartment,
      "comment_client": this.clientForm.value.comment_client
    }

    this.service.getInfoForOrder(params).subscribe(data => {
      console.log(data);
      
    })
  }
}
