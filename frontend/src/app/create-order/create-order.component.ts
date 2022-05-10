import { Component, OnInit } from '@angular/core';
import { DatepickerOptions } from 'ng2-datepicker';
import locale from 'date-fns/locale/en-US';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-create-order',
  templateUrl: './create-order.component.html',
  styleUrls: ['./create-order.component.sass']
})
export class CreateOrderComponent implements OnInit {

  constructor(private fb: FormBuilder) { }

  orderForm: FormGroup;
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

  ngOnInit(): void {
    this.orderForm = this.fb.group({
      kod_model: '',
      kolor_model: '',
      name_color: '',
      id_color_part_1: '',
      id_color_part_2: '',
      price_model: '',
      quantity_pars_model: ''
    })
  }

  addOrder() {
    this.orders.push(1);
  }

  deleteOrder() {
    this.orders.pop()
  }
}
