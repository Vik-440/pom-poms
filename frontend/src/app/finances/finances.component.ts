import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
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
  mainItems;
  periods: string[];
  outlayData;
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

    this.service.getFinances().subscribe((data: any) => {
      const copyData = data.slice(0);
      this.metodPayment = data[0].metod_payment;
      this.outlayData = data[data.length - 1];
      this.mainItems = copyData.slice(1, data.length - 1);
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
      this.mainItems = data;
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

}
