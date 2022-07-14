import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
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
      metod: null,
      data_start: '',
      data_end: '',
      period: null,
      id_order: null
    });
    this.spendingForm = this.fb.group({
      data_start: '',
      data_end: ''
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
    console.log(this.removeEmptyValues(params));
    this.service.getFilters(params).subscribe((data: any) => {
      this.mainItems = data;
    })
    
  }

}
