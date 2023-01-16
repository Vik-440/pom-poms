import { Component, OnInit, TemplateRef } from '@angular/core';
import { MainPageService } from '../services/main-table.service';
import { NgbCalendar, NgbDate, NgbDatepickerModule, NgbDateStruct, NgbOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import * as _ from 'lodash';
import * as moment from 'moment';
import { FormBuilder, FormGroup, FormsModule } from '@angular/forms';

@Component({
    selector: 'app-main-table',
    templateUrl: './main-table.component.html',
    styleUrls: ['./main-table.component.sass'],
})
export class MainTableComponent implements OnInit {
    orders = [];
    isShowSpinner = false;
    closeResult = '';
    isShowFilter = false;
    alert = {
        type: '',
        message: '',
        isShow: false,
    };
    queue = 0;
    dateDownloaded;
    speed;
    todayYear = new Date().getFullYear();
    filtersForm: FormGroup;
    model: NgbDateStruct;

    constructor(
        private service: MainPageService,
        private offcanvasService: NgbOffcanvas,
        private fb: FormBuilder,
        private calendar: NgbCalendar
    ) {}

    ngOnInit(): void {
        this.getAllData();
        this.initForm();
    }

    isDisabled = (date: NgbDate, current: { month: number; year: number }) => date.month !== current.month;
	isWeekend = (date: NgbDate) => this.calendar.getWeekday(date) >= 6;
    
    initForm() {
        this.filtersForm = this.fb.group({
            dataStart: '',
            dataEnd: '',
            fulfilled_order: '',
            phone_client: '',
        });
    }
    openFilterMenu(content: TemplateRef<any>) {
        this.isShowFilter = true;
        this.offcanvasService.open(content, { position: 'end' });
    }

    closeFilterMenu() {
        this.offcanvasService.dismiss();
        this.isShowFilter = false;
    }

    clickOutsidePhaseSingle(index, phase, order, phaseEl) {
        phaseEl.value = order[phase];
        const cloneOrderPhase = _.cloneDeep(order[phase]);
        this.orders[index][phase] = cloneOrderPhase;
        this.orders = this.orders;
    }

    clickOutsidePhaseMultiply(indexPhase, phase, order, phaseEl) {
        (document.getElementById(phaseEl) as HTMLInputElement).value = order[phase][indexPhase];
    }

    changePhase(item, phase, event) {
        if (event && event.type == 'click') {
            event.target.value = '';
        } else {
            this.orders.forEach((order) => {
                if (order.id_order === item.id_order) {
                    order = {
                        ...order,
                        [phase]: order[order],
                    };
                }
            });
        }
    }

    changePhases(phase, event, item) {
        if (event && event.type == 'click') {
            event.target.value = '';
        } else {
            this.orders.forEach((order) => {
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
            [phase]: [item[phase] - e.target.value],
        };

        this.service.changePhase(item.id_order, params).subscribe((data: any) => {
            if (data.check_sum_phase === params[phase][0]) {
                this.alert = {
                    isShow: true,
                    type: 'success',
                    message: 'Дані змінено',
                };
                setTimeout(() => {
                    this.alertChange(false);
                }, 3000);
                this.orders = this.orders.map((order) => {
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
                    message: 'Дані не збігаються',
                };
            }
            setTimeout(() => {
                this.alertChange(false);
            }, 3000);
        });
    }

    getAllData() {
        this.isShowSpinner = true;
        this.service.getListMain().subscribe(
            (data: any) => {
                this.orders = data;
                this.isShowSpinner = false;
            },
            () => {
                this.isShowSpinner = false;
            }
        );
    }

    getSumPhases(phase) {
        let sum = 0;
        this.orders.map((item) => {
            if (!item.fulfilled_order) {
                sum += Array.isArray(item[phase])
                    ? item[phase].reduce((partialSum, a) => partialSum + a, 0)
                    : item[phase];
            }
        });
        return sum;
    }

    isArray(array) {
        return Array.isArray(array);
    }

    getColorForMoney(order) {
        const interest = (100 * order.real_money) / order.sum_payment;
        if (interest < 10) {
            return 'red';
        } else if (interest >= 100) {
            return 'green';
        }
    }

    getMoney(sum) {
        return Number(sum).toFixed(sum.toString().endsWith('.00') ? null : 2);
    }

    isHasCity(city) {
        return city.includes('самовивіз');
    }

    tooltipCity(order) {
        const regexPhone = /(\d{2})(\d{3})(\d{3})(\d{2})(\d{2})/g;
        const tooltip = [
            'Н.П. №' + order.np_number,
            order.first_name_client + ' ' + order.second_name_client,
            order.phone_recipient.replace(regexPhone, '$1-' + '$2-' + '$3-' + '$4-' + '$5'),
            order.zip_code,
            order.street_house_apartment,
        ];
        return tooltip.filter((data) => data).join('\n');
    }

    changeHeight(j, i) {
        return {
            height: `${document.querySelectorAll(`#kolorModel-${j}-${i}`)[0].clientHeight}px`,
        };
    }

    checkCode(kodModel, commentModel) {
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

    getFulfilledOrder() {
        let sum = 0;
        this.orders.map((item) => {
            if (!item.fulfilled_order) {
                sum += Array.isArray(item.phase_1)
                    ? item.phase_1.reduce((partialSum, a) => partialSum + a, 0)
                    : item.phase_1;
            }
        });
        this.queue = sum / 2;
        return this.queue;
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

    removeData(control) {
        this.filtersForm.get(control).patchValue('');
    }

    alertChange(e) {
        this.alert.isShow = e;
    }
}
