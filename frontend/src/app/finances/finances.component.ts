import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
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
  paymentFrom;
  spendingForm;
  mainItems;
  periods: string[];
  outlayData;
  todayYear = new Date().getFullYear();
  ngOnInit(): void {
    this.paymentFrom = this.fb.group({
      metod: '',
      dateFrom: '',
      dateTo: '',
      period: '',
      numberOrder: ''
    });
    this.spendingForm = this.fb.group({
      dateFrom: '',
      dateTo: ''
    })
    this.service.getFinances().subscribe((data: any) => {
      const copyData = data.slice(0);
      this.metodPayment = data[0].metod_payment;
      this.outlayData = data[data.length - 1];
      this.mainItems = copyData.slice(1, data.length - 1);
    })
    this.periods = ['день', 'тиждень', 'місяць', 'квартал', 'рік']
  }

  click() {
  }

}
