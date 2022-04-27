import { Component, OnInit } from '@angular/core';
import { DatepickerOptions } from 'ng2-datepicker';
import locale from 'date-fns/locale/en-US';

@Component({
  selector: 'app-create-order',
  templateUrl: './create-order.component.html',
  styleUrls: ['./create-order.component.sass']
})
export class CreateOrderComponent implements OnInit {

  constructor() { }

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

  isRecipient = false;
  ngOnInit(): void {
  }

  addOrder() {
    this.orders.push(1);
  }

  deleteOrder() {
    this.orders.pop()
  }
}
