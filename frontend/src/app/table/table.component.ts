import { Component, Directive, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { NgbCalendar, NgbDate, NgbDateParserFormatter } from '@ng-bootstrap/ng-bootstrap';
import locale from 'date-fns/locale/en-US';
import * as moment from 'moment';
import { DatepickerOptions } from 'ng2-datepicker';
import * as _ from 'lodash'
import { CreateOrderService } from '../services/create-order.service';
import { MainPage } from '../services/main-table.service';
import { logging } from 'protractor';
interface OrderInterface {
    id_order: number;
    data_order: string;
    kolor_model: string[] | string;
    kod_model: string[] | string;
    comment_model: string[] | string;
    kolor_cell_model: string[] | string;
    quantity_pars_model: number[] | number;
    kolor_cell_pars: string[] | string;
    phase_1: number;
    phase_2: number;
    phase_3: number;
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


export type SortColumn = keyof OrderInterface | '';
export type SortDirection = 'asc' | 'desc' | '';
const rotate: { [key: string]: SortDirection } = { asc: 'desc', desc: '', '': 'asc' };

export interface SortEvent {
    column: SortColumn;
    direction: SortDirection;
}

@Directive({
    selector: 'th[sortable]',
    host: {
        '[class.asc]': 'direction === "asc"',
        '[class.desc]': 'direction === "desc"',
        '(click)': 'rotate()',
    },
})
export class SortDirective {
    @Input() sortable: SortColumn = '';
    @Input() direction: SortDirection = '';
    @Output() sort = new EventEmitter<SortEvent>();

    rotate() {
        this.direction = rotate[this.direction];
        this.sort.emit({ column: this.sortable, direction: this.direction });
    }
}

@Component({
    selector: 'app-table',
    templateUrl: './table.component.html',
    styleUrls: ['./table.component.sass'],
})
export class TableComponent implements OnInit, OnDestroy {
    @ViewChild('dataStart') dataStart;
    @ViewChild('dataEnd') dataEnd;
    filtersForm: FormGroup;
    alert = {
        type: '',
        message: '',
        isShow: false
    }
    ordersRow = [];
    switchConfig = {
        labels: {
            unchecked: 'OFF',
            checked: 'ON',
        },
        switchColor: {
            checked: '#32FA00',
            unchecked: '#FA0000',
        },
        color: {
            unchecked: '#C4C4C4',
            checked: '#C4C4C4',
        },
        width: 80,
        height: 35,
        fontSize: 16,
    };
    hoveredDate: NgbDate | null = null;

    fromDate: NgbDate | null;
    toDate: NgbDate | null;
    date = new Date();
    todayYear = new Date().getFullYear();
    options: DatepickerOptions = {
        minDate: new Date(''),
        format: 'yyyy-MM-dd',
        formatDays: 'EEEEE',
        firstCalendarDay: 1, // 0 - Sunday, 1 - Monday
        locale: locale,
        position: 'bottom',
        placeholder: '',
        calendarClass: 'datepicker-default',
        scrollBarColor: '#dfe3e9',
    };

    isShowCalendar = false;

    dataDateForm: FormGroup;
    phoneClients = [];
    dateDownloaded = '';
    speed: number;
    queue: number = 0;
    fulfilledOrderItems = [
        { id: 1, value: true, name: 'виконані' },
        { id: 2, value: false, name: 'всі' },
        { id: 3, value: '', name: 'не виконані' },
    ];

    constructor(
        private fb: FormBuilder,
        private service: MainPage,
        private calendar: NgbCalendar,
        public formatter: NgbDateParserFormatter,
        private serviceOrders: CreateOrderService
    ) {}

    ngOnInit() {
        this.filtersForm = this.fb.group({
            dataStart: '',
            dataEnd: '',
            fulfilled_order: '',
            phone_client: '',
        });

        this.service.getListMain().subscribe((data: any) => {
            this.ordersRow = data;
        });

        this.dataDateForm = this.fb.group({
            dateStart: null,
            dateEnd: null,
        });
    }

    ngOnDestroy() {
        this.ordersRow = [];
    }

    changeDate(value) {
        this.dataDateForm = this.fb.group({
            dateStart: null,
            dateEnd: null,
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
        return (
            this.fromDate &&
            !this.toDate &&
            this.hoveredDate &&
            date.after(this.fromDate) &&
            date.before(this.hoveredDate)
        );
    }

    isInside(date: NgbDate) {
        return this.toDate && date.after(this.fromDate) && date.before(this.toDate);
    }

    isRange(date: NgbDate) {
        return (
            date.equals(this.fromDate) ||
            (this.toDate && date.equals(this.toDate)) ||
            this.isInside(date) ||
            this.isHovered(date)
        );
    }

    validateInput(currentValue: NgbDate | null, input: string): NgbDate | null {
        const parsed = this.formatter.parse(input);
        return parsed && this.calendar.isValid(NgbDate.from(parsed)) ? NgbDate.from(parsed) : currentValue;
    }

    checkArray(array) {
        return Array.isArray(array);
    }

    countMoney(order) {
        const interest = (100 * order.real_money) / order.sum_payment;
        if (interest < 25) {
            return 'red';
        } else if (interest >= 100) {
            return 'green';
        }
    }

    checkCode(kodModel, commentModel, i?) {
        if (commentModel) {
            return 'yellow';
        }
        const letterModel = kodModel.split('');
        if (+letterModel[2] !== 0) {
            return 'light-pink';
        }
        const splitModelH = kodModel.split('-');
        if (splitModelH[1]?.split('')[0] === 'В' || splitModelH[1]?.split('')[0] === 'B') {
            return 'light-blue';
        }

        return '';
    }

    getMoney(sum) {
        return Number(sum).toFixed(sum.toString().endsWith('.00') ? null : 2);
    }
    getFulfilledOrder() {
        let sum: number = 0;
        this.ordersRow.map((item) => {
            if (!item.fulfilled_order) {
                sum += Array.isArray(item.quantity_pars_model)
                    ? item.quantity_pars_model.reduce((partialSum, a) => partialSum + a, 0)
                    : item.quantity_pars_model;
            }
        });
        this.queue = sum;
        return sum;
    }

    sityColor(city) {
        return city.includes('самовивіз');
    }

    editData(data) {
        return data
            .map((item) => {
                if (item <= 9) {
                    return '0' + item;
                }
                return item;
            })
            .join('-');
    }

    applyFilters() {
        let params: any = {
            data_start: this.editData(Object.values(this.filtersForm.value.dataStart)),
            data_end: this.editData(Object.values(this.filtersForm.value.dataEnd)),
            fulfilled_order: this.filtersForm.value.fulfilled_order,
        };
        if (this.filtersForm.value.fulfilled_order === '') {
            delete params.fulfilled_order;
        }

        if (this.filtersForm.value.dataStart === '') {
            delete params.data_start;
        }

        if (this.filtersForm.value.dataEnd === '') {
            delete params.data_end;
        }

        if (this.filtersForm.value.phone_client) {
            params = {
                ...params,
                phone_client: this.filtersForm.value.phone_client,
            };
        }
        this.service.getListWithFilters(params).subscribe((data: any) => {
            this.ordersRow = data;
        });
    }

    changeSpeed() {
        const days = Math.ceil(this.queue / this.speed);
        this.dateDownloaded = moment().weekday(0).add(days, 'days').format('YYYY-MM-DD');
    }

    makeDone(id, fulfilledOrder, i) {
        this.service.makeDoneOrder({ fulfilled_id_order: id, fulfilled_order: fulfilledOrder }).subscribe(() => {
            this.ordersRow.forEach((order, index) => {
                if (i === index) {
                    order.fulfilled_order = !order.fulfilled_order;
                }
            });
        });
    }

    tooltipCity(order) {
        const tooltip = [
            'Н.П. №' + order.np_number,
            order.first_name_client + ' ' + order.second_name_client,
            order.phone_recipient,
            order.zip_code,
            order.street_house_apartment,
        ];
        return tooltip.filter((n) => n).join(', ');
    }

    changePhone(event) {
        if (event.term.length >= 4) {
            this.serviceOrders.getInfoForOrder({ ur_phone: event.term }).subscribe((numbers: any) => {
                this.phoneClients = numbers?.phone_client;
            });
        }
    }

    removeData(control) {
        this.options = {
            ...this.options,
        };
        this.filtersForm.get(control).patchValue('');
    }


    changePhases(order, indexPhase, phase, event, item) {
        if(event && event.type == 'click') {
            event.target.value = '';

        } else {
            this.ordersRow.forEach((order) => {
                if(order.id_order === item.id_order) {
                    order = {
                        ...order,
                        [phase]: order[order],
                    }
                }
            })
        }     
    }

    changePhase(item, phase, e, item2) {
        if(e && e.type == 'click') {
            e.target.value = '';

        } else {
            this.ordersRow.forEach((order) => {
                if(order.id_order === item.id_order) {
                    order = {
                        ...order,
                        [phase]: order[order],
                    }
                }
            })
        }
    }

    sendPhase(item, phase, e) {
        const params = {
            [phase]: [item[phase] - e.target.value]
        };
  
        
        this.service.sendPhase(item.id_order, params).subscribe((data: any) => {
            if(data.check_sum_phase === params[phase][0]) {
                this.alert = {
                    isShow: true,
                    type: 'success',
                    message: 'Дані змінено'
                };
                this.ordersRow = this.ordersRow.map((order, index) => {
                    if(order.id_order === item.id_order) {
                        order = {
                            ...order,
                            [phase]: params[phase][0],
                        }
                        item[phase] = params[phase][0]
                    }
                    return order;
                })
            } else {
                this.alert = {
                    isShow: true,
                    type: 'danger',
                    message: 'Дані не збігаються'
                };
            }
            setTimeout(() => {
                this.alertChange(false);
            }, 3000);
        });
    }

    sendPhases(order, phaseIndex, phase, event, item) {
        const params = [...order[phase]];
        params[phaseIndex] = item - event.target.value;

        this.service.sendPhase(order.id_order, {[phase]: params}).subscribe((data: any) => {
            if(data.check_sum_phase === params.reduce( (accumulator, currentValue) => accumulator + currentValue)) {
                this.alert = {
                    isShow: true,
                    type: 'success',
                    message: 'Дані змінено'
                };
    
                this.ordersRow = this.ordersRow.map((orderItem, index) => {
                    if(orderItem.id_order === order.id_order) {   
                        orderItem = {
                            ...orderItem,
                            [phase]: [...params],
                        }
                    }
                    return orderItem;
                });
            } else {
                this.alert = {
                    isShow: true,
                    type: 'danger',
                    message: 'Дані не збігаються'
                };
            }
            setTimeout(() => {
                this.alertChange(false);
            }, 3000);
        })
    }

    click2(e, item, q) {

if(item) {
    this.ordersRow.forEach((order) => {
        if(order.id_order === item.id_order) {
            order = {
                ...order,
                phase_1: 3,
            }
            
        }
    })
    // this.ordersRow[0].phase_1 = 3
}
        
        
    }

    clickO(index, phase, order, phaseEl) {

        phaseEl.value = order[phase];

const a = _.cloneDeep(order[phase]);

        this.ordersRow[index][phase] = a    
        this.ordersRow = this.ordersRow;
    
    }

    clickOutside(indexPhase, phase, order, phaseEl) {
        (document.getElementById(phaseEl) as HTMLInputElement).value = order[phase][indexPhase];
    }

    alertChange(e) {
        this.alert.isShow = e;    
    }

    changeHeight(j, i) {
        return {
            height: `${document.querySelectorAll(`#kolorModel-${j}-${i}`)[0].clientHeight}px`,
        };
    }
}
