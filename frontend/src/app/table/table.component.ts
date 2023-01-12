import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { NgbCalendar, NgbDate, NgbDateParserFormatter } from '@ng-bootstrap/ng-bootstrap';
import locale from 'date-fns/locale/en-US';
import * as _ from 'lodash';
import * as moment from 'moment';
import { DatepickerOptions } from 'ng2-datepicker';
import { NgxSpinnerService } from 'ngx-spinner';
import { CreateOrderService } from '../services/create-order.service';
import { MainPageService } from '../services/main-table.service';

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
    };
    isShowSpinner = false;
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
        locale,
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
    queue = 0;
    fulfilledOrderItems = [
        { id: 1, value: true, name: 'виконані' },
        { id: 2, value: false, name: 'всі' },
        { id: 3, value: '', name: 'не виконані' },
    ];

    constructor(
        private fb: FormBuilder,
        private service: MainPageService,
        private calendar: NgbCalendar,
        public formatter: NgbDateParserFormatter,
        private serviceOrders: CreateOrderService,
        private spinner: NgxSpinnerService
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
        if (interest < 10) {
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
        let sum = 0;
        this.ordersRow.map((item) => {
            if (!item.fulfilled_order) {
                sum += Array.isArray(item.phase_1)
                    ? item.phase_1.reduce((partialSum, a) => partialSum + a, 0)
                    : item.phase_1;
            }
        });
        this.queue = sum / 2;
        return sum / 2;
    }

    getSumPhases(phase){
        let sum = 0;
        this.ordersRow.map((item) => {
            if (!item.fulfilled_order) {
                sum += Array.isArray(item[phase])
                    ? item[phase].reduce((partialSum, a) => partialSum + a, 0)
                    : item[phase];
            }
        });
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
        this.isShowSpinner = true;
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
            this.isShowSpinner = false;
        });
    }

    changeSpeed() {
        const days = Math.ceil(this.queue / this.speed);
        this.dateDownloaded = this.addWeekdays(Number.isFinite(days) ? days : 0);
    }

    addWeekdays(days) {
        let date = moment().add(1, 'days');
        while (days > 0) {
            if (date.isoWeekday() !== 7) {
                days -= 1;
            }
            date = date.add(1, 'days');
        }
        return date.isoWeekday() === 7 ? date.add(1, 'days').format('YYYY-MM-DD') : date.format('YYYY-MM-DD');
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
        const regexPhone = /(\d{2})(\d{3})(\d{3})(\d{2})(\d{2})/g;
        const tooltip = [
            'Н.П. №' + order.np_number ,
            order.first_name_client + ' ' + order.second_name_client,
            order.phone_recipient.replace(regexPhone, '$1-' + '$2-' + '$3-' + '$4-' + '$5'),
            order.zip_code,
            order.street_house_apartment,
        ];
        return tooltip.filter((data) => data).join('\n');
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
        if (event && event.type == 'click') {
            event.target.value = '';

        } else {
            this.ordersRow.forEach((order) => {
                if (order.id_order === item.id_order) {
                    order = {
                        ...order,
                        [phase]: order[order],
                    };
                }
            });
        }
    }

    changePhase(item, phase, e, item2) {
        if (e && e.type == 'click') {
            e.target.value = '';

        } else {
            this.ordersRow.forEach((order) => {
                if (order.id_order === item.id_order) {
                    order = {
                        ...order,
                        [phase]: order[order],
                    };
                }
            });
        }
    }

    sendPhase(item, phase, e) {
        const params = {
            [phase]: [item[phase] - e.target.value]
        };


        this.service.sendPhase(item.id_order, params).subscribe((data: any) => {
            if (data.check_sum_phase === params[phase][0]) {
                this.alert = {
                    isShow: true,
                    type: 'success',
                    message: 'Дані змінено'
                };
                setTimeout(() => {
                    this.alertChange(false);
                }, 3000);
                this.ordersRow = this.ordersRow.map((order, index) => {
                    if (order.id_order === item.id_order) {
                        order = {
                            ...order,
                            [phase]: params[phase][0],
                        };
                        item[phase] = params[phase][0];
                    }
                    return order;
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
        });
    }

    sendPhases(order, phaseIndex, phase, event, item) {
        const params = [...order[phase]];
        params[phaseIndex] = item - event.target.value;

        this.service.sendPhase(order.id_order, {[phase]: params}).subscribe((data: any) => {
            if (data.check_sum_phase === params.reduce( (accumulator, currentValue) => accumulator + currentValue)) {
                this.alert = {
                    isShow: true,
                    type: 'success',
                    message: 'Дані змінено'
                };
                setTimeout(() => {
                    this.alertChange(false);
                }, 3000);
                this.ordersRow = this.ordersRow.map((orderItem, index) => {
                    if (orderItem.id_order === order.id_order) {
                        orderItem = {
                            ...orderItem,
                            [phase]: [...params],
                        };
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
        });
    }

    click2(e, item, q) {

if (item) {
    this.ordersRow.forEach((order) => {
        if (order.id_order === item.id_order) {
            order = {
                ...order,
                phase_1: 3,
            };

        }
    });
    // this.ordersRow[0].phase_1 = 3
}


    }

    clickO(index, phase, order, phaseEl) {

        phaseEl.value = order[phase];

        const a = _.cloneDeep(order[phase]);

        this.ordersRow[index][phase] = a;
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
