import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as _ from 'lodash';
import { FinancesPageService } from '../services/finances.service';

@Component({
  selector: 'app-finances',
  templateUrl: './finances.component.html',
  styleUrls: ['./finances.component.sass']
})
export class FinancesComponent implements OnInit {

  constructor(private service: FinancesPageService, private fb: FormBuilder) { }

  items = [];
  metodPayment;
  paymentFrom: FormGroup;
  spendingForm;
  dataItems: FormArray;
  periods: string[];
  outlayData;
  itemEdit;
  datePrevious = {
    year: new Date().getFullYear(),
    day: new Date().getDay(),
    month: new Date().getMonth()
  };
  todayYear = new Date().getFullYear();
  ngOnInit(): void {
    
    this.paymentFrom = this.fb.group({
      metod: [null, Validators.required],
      data_start: [null, Validators.required],
      data_end: [null, Validators.required],
      period: [null, Validators.required],
      id_order: null
    });
    this.spendingForm = this.fb.group({
      data_start: [null, Validators.required],
      data_end: [null, Validators.required]
    })

    this.dataItems = this.fb.array([this.fb.group({
      data_payment: [null, Validators.required],
      metod_payment: ['iban', Validators.required],
      id_order: [null, Validators.required],
      id_payment: null,
      payment: [null, Validators.required],
      status: 'edit'
    })])
    this.service.getFinances().subscribe((data: any) => {
      const copyData = data.slice(0);
      this.metodPayment = data[0].metod_payment;
      this.outlayData = data[data.length - 1];
      const mainItems = copyData.slice(1, data.length - 1);
      if(mainItems.length) {
        this.dataItems.clear()
        mainItems.forEach((item, i) => {
          const dataArray = item.data_payment.split('-')
          this.dataItems.push(this.fb.group({
            data_payment: [{ year: +dataArray[0], month: +dataArray[1], day: +dataArray[2] }, Validators.required],
            metod_payment: [item.metod_payment, Validators.required],
            id_payment: [item.id_payment],
            id_order: [item.id_order, Validators.required],
            payment: [item.payment, Validators.required],
            status: 'edit'
          }));
        });
        this.datePrevious = JSON.parse(localStorage.getItem('date_payment')) || null;
        this.dataItems.push(this.fb.group({
          data_payment: [this.datePrevious, Validators.required],
          metod_payment: ['iban', Validators.required],
          id_order: [null, Validators.required],
          id_payment: null,
          payment: [null, Validators.required],
          status: 'ok'
          }))
      }
    })
    this.periods = ['день', 'тиждень', 'місяць', 'квартал', 'рік']
  }

  removeEmptyValues(object) {
    const newObject = {
      ...object
    };
    for (var key in newObject) {
        if (newObject.hasOwnProperty(key)) {
            var value = newObject[key];
            if (value === null || value === undefined || value === '') {
                delete newObject[key];
            }
        }
    }
    return newObject;
}


  sendFiltersPayments() {

    let params = {
      ...this.paymentFrom.value,
      data_start: this.editData(Object.values(this.paymentFrom.value.data_start)),
      data_end: this.editData(Object.values(this.paymentFrom.value.data_end)),
      payment_search: 0,
      iban: this.paymentFrom.value.metod === 'iban',
      cash: this.paymentFrom.value.metod === 'cash'
    };

    if(this.paymentFrom.value.id_order) {
      params = {
        id_order: this.paymentFrom.value.id_order
      }
    }
    delete params['metod'];
    this.service.getFilters(params).subscribe((data: any) => {
      // this.mainItems = data;
    })
  }

  editData(data) {
    return data.map((item) => {
      if(item <= 9) {
        return '0' + item
      }
      return item
    }).join('-')
  }
  sendSpendingFilters() {
    const params = {
      data_start: this.editData(Object.values(this.spendingForm.value.data_start)),
      data_end: this.editData(Object.values(this.spendingForm.value.data_end)),
      outlay_search: 0
    }
    this.service.getFilters(params).subscribe((data: any) => {
      // this.mainItems = data;
    })
  }

  actionClick(action, item) {
    if(action === 'edit') {
      this.itemEdit = _.cloneDeep(item.value);
      item.patchValue({
        status: 'process'
      });
    } else if (action === 'close') {
      item.patchValue({
        ...this.itemEdit,
        status: 'edit'
      }); 
    } else if (action === 'edited') {
      const params = {
        id_payment: item.value.id_payment,
        data_payment: item.value.data_payment,
        metod_payment: item.value.metod_payment,
        id_order: item.value.id_order,
        payment: item.value.payment
      };

      this.service.editPayment(params).subscribe(() => {
        item.patchValue({
          status: 'edit'
        })
      })
    } else if (action === 'ok') {
      localStorage.setItem('date_payment', JSON.stringify(this.dataItems.value.data_payment)); 
      this.dataItems.push(this.fb.group({
        data_payment: [this.datePrevious, Validators.required],
        metod_payment: 'iban',
        id_payment: null,
        id_order: [null, Validators.required],
        payment: [null, Validators.required],
        status: 'ok'
      }))
    }
  }

  savePayment() {
    const paymentForSave = this.dataItems.value[this.dataItems.value.length - 1];
    const params = {
      data_payment: this.editData(Object.values(paymentForSave.data_payment)),
      metod_payment: paymentForSave.metod_payment,
      id_order: +paymentForSave.id_order,
      payment: +paymentForSave.payment
    }
    this.service.savePayment(params).subscribe(() => {

    })
  }
}
