import { Component, OnInit } from '@angular/core';
import { DatepickerOptions } from 'ng2-datepicker';
import locale from 'date-fns/locale/en-US';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';
import { tap } from 'rxjs';
import { CreateOrderService } from '../services/create-order.service';

@Component({
  selector: 'app-create-order',
  templateUrl: './create-order.component.html',
  styleUrls: ['./create-order.component.sass']
})
export class CreateOrderComponent implements OnInit {

  constructor(private fb: FormBuilder, private service: CreateOrderService) { }

  orderForm: FormArray;
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
}
