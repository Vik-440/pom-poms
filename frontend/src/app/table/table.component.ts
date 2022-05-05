import { Component, Directive, EventEmitter, Input, OnDestroy, OnInit, Output, QueryList, ViewChildren } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { MainPage } from '../services/main-table.service';
import {NgbDate, NgbCalendar, NgbDateParserFormatter} from '@ng-bootstrap/ng-bootstrap';
import { ComponentFactoryResolver } from '@angular/core';
import { DatepickerOptions } from 'ng2-datepicker';
import locale from 'date-fns/locale/en-US';
import { FormBuilder, FormGroup } from '@angular/forms';
import { tap } from 'rxjs';

interface OrderInterface {
  id_order: number;
  data_order: string;
  kolor_model: string[] | string;
  kod_model: string[] | string;
  comment_model: string[] | string;
  kolor_cell_model: string[] | string;
  quantity_pars_model: number[] | number;
  kolor_cell_pars: string[] | string;
  phase_1_model: boolean[] | boolean;
  phase_2_model: boolean[] | boolean;
  phase_3_model: boolean[] | boolean;
  sum_payment: number;
  real_money: number;
  left_money: number;
  telephone: string;
  sity: string[] | string;
  data_plane_order: string;
  fulfilled_order: boolean;
  comment_order: number[] | number;
}

const orders: OrderInterface[] = [];

export type SortColumn = keyof OrderInterface | '';
export type SortDirection = 'asc' | 'desc' | '';
const rotate: {[key: string]: SortDirection} = { 'asc': 'desc', 'desc': '', '': 'asc' };

const compare = (v1: any, v2: any) => v1 < v2 ? -1 : v1 > v2 ? 1 : 0;

export interface SortEvent {
  column: SortColumn;
  direction: SortDirection;
}

@Directive({
  selector: 'th[sortable]',
  host: {
    '[class.asc]': 'direction === "asc"',
    '[class.desc]': 'direction === "desc"',
    '(click)': 'rotate()'
  }
})
export class SortDirective {

  @Input() sortable: SortColumn = '';
  @Input() direction: SortDirection = '';
  @Output() sort = new EventEmitter<SortEvent>();

  rotate() {
    this.direction = rotate[this.direction];
    this.sort.emit({column: this.sortable, direction: this.direction});
  }
}

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.sass']
})
export class TableComponent implements OnInit, OnDestroy {

  ordersRow = [];
  switchConfig = {
    labels: {
      unchecked: "OFF",
      checked: "ON"
    },
    switchColor: {
      checked: "#32FA00",
      unchecked: "#FA0000"
    },
    color: {
      unchecked: '#C4C4C4',
      checked: '#C4C4C4'
    },
    width: 80,
    height: 35,
    fontSize: 16
  }
  hoveredDate: NgbDate | null = null;

  fromDate: NgbDate | null;
  toDate: NgbDate | null;
  date = new Date();
  options: DatepickerOptions = {
    minDate: new Date(''),
    format: 'MM/dd/yyyy', // date format to display in input
    formatDays: 'EEEEE',
    firstCalendarDay: 1, // 0 - Sunday, 1 - Monday
    locale: locale,
    position: 'bottom',
    placeholder: 'mm/dd/yyyy',
    inputClass: '', // custom input CSS class to be applied
    calendarClass: 'datepicker-default', // custom datepicker calendar CSS class to be applied
    scrollBarColor: '#dfe3e9', // in case you customize you theme, here you define scroll bar color
    // keyboardEvents: true // enable keyboard events
  };

  isShowCalendar = false;
  optionsDateStart: DatepickerOptions;
  optionsDateEnd: DatepickerOptions;

  dataDateForm: FormGroup;
  @ViewChildren(SortDirective) headers: QueryList<SortDirective>;

  constructor(
    private fb: FormBuilder,
    private resolver: ComponentFactoryResolver, private httpClient: HttpClient, private service: MainPage, private calendar: NgbCalendar, public formatter: NgbDateParserFormatter){

  }

  ngOnInit() {
    this.service.getList().subscribe();
    this.dataDateForm = this.fb.group({
      dateStart: null,
      dateEnd: null
    });

    console.log(this.ordersRow)
    this.httpClient.get("assets/tmp.json").subscribe(data =>{
      Object.values(data).forEach(row => {
        this.ordersRow.push({
          id_order: row.id_order || '',
          data_order: row.data_order || '',
          kolor_model: row.kolor_model || '',
          kod_model: row.kod_model || '',
          comment_model: row.comment_model || '',
          kolor_cell_model: row.kolor_cell_model || '',
          quantity_pars_model: row.quantity_pars_model || '',
          kolor_cell_pars: row.kolor_cell_pars || '',
          phase_1_model: row.phase_1_model || '',
          phase_2_model: row.phase_2_model || '',
          phase_3_model: row.phase_3_model || '',
          sum_payment: row.sum_payment || '',
          real_money: row.real_money || 0,
          left_money: row.sum_payment - row.real_money,
          telephone: '',
          sity: row.sity || '',
          data_plane_order: row.data_plane_order || '',
          fulfilled_order: row.fulfilled_order || '',
          comment_order: row.comment_order || '',
        })
      });
    })

    this.optionsDateStart = {
      ...this.options
    }

    this.optionsDateEnd = {
      ...this.options
    }
    this.dataDateForm.valueChanges.pipe(
      tap(value => {
        this.optionsDateStart = {
          ...this.optionsDateStart,
          maxDate: new Date(value.dateEnd)
        }

        this.optionsDateEnd = {
          ...this.optionsDateEnd,
          minDate: new Date(value.dateStart)
        }
      })
    ).subscribe();
 }

 ngOnDestroy(){
   this.ordersRow = [];
 }

 changeDate(value){
  console.log('value', value);
  this.dataDateForm = this.fb.group({
    dateStart: null,
    dateEnd: null
  });
 }

 onDateSelection(date: NgbDate) {
  if (!this.fromDate && !this.toDate) {
    this.fromDate = date;
  } else if (this.fromDate && !this.toDate && date && date.after(this.fromDate)) {
    this.toDate = date;
  } else {
    this.toDate = null;
    this.fromDate = date;
  }
}

isHovered(date: NgbDate) {
  return this.fromDate && !this.toDate && this.hoveredDate && date.after(this.fromDate) &&
      date.before(this.hoveredDate);
}

isInside(date: NgbDate) { return this.toDate && date.after(this.fromDate) && date.before(this.toDate); }

isRange(date: NgbDate) {
  return date.equals(this.fromDate) || (this.toDate && date.equals(this.toDate)) || this.isInside(date) ||
      this.isHovered(date);
}

validateInput(currentValue: NgbDate | null, input: string): NgbDate | null {
  const parsed = this.formatter.parse(input);
  return parsed && this.calendar.isValid(NgbDate.from(parsed)) ? NgbDate.from(parsed) : currentValue;
}

  checkArray(array) {
    return Array.isArray(array);
  }

  countMoney(order) {
    const interest = (100*order.real_money)/order.sum_payment;
    if(interest < 25) {
      return 'red';
    } else if(interest === 100) {
      return 'green';
    } else {
      return 'yellow';
    }
  }

  checkCode(kodModel, commentModel, i?) {
    const classListArray = [];
    if(commentModel) {
      classListArray.push('y');
    }
    const letterModel = kodModel.split('');
      if(+letterModel[2] !== 0){
        classListArray.push('cr')
    }
    const splitModelH = kodModel.split('-');
    if(splitModelH[1].split('')[0] === 'B') {
      classListArray.push('lb');
    }

    return classListArray.join('-');
  }

  onSort({column, direction}: SortEvent) {
    this.headers.forEach(header => {
      if (header.sortable !== column) {
        header.direction = '';
      }
    });

    // sorting countries
    if (direction === '' || column === '') {
      this.ordersRow = orders;
    } else {
      this.ordersRow = [...orders].sort((a, b) => {
        const res = compare(a[column], b[column]);
        return direction === 'asc' ? res : -res;
      });
    }
  }

}
