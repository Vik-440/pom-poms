import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as _ from 'lodash';
import * as moment from 'moment';
import { FinancesPageService } from '../services/finances.service';

@Component({
    selector: 'app-finances',
    templateUrl: './finances.component.html',
    styleUrls: ['./finances.component.sass'],
})
export class FinancesComponent implements OnInit {
    constructor(private service: FinancesPageService, private fb: FormBuilder) {}

    metodPayment = [];
    outlayClass: string[];
    paymentFrom: FormGroup;
    spendingForm;
    dataItems: FormArray;
    periods: string[];
    outlayData: FormArray;
    statisticsPeriods;
    statisticsData;
    isShowStatistics = false;
    statisticsPayments = [];
    itemEdit;
    datePrevious = {
        year: new Date().getFullYear(),
        day: new Date().getDay(),
        month: new Date().getMonth(),
    };
    todayYear = new Date().getFullYear();

    ngOnInit(): void {
        this.service.getMethods().subscribe((data: any) => {
            this.metodPayment = data.metod_payment;
            this.outlayClass = data.outlay_class;
            this.periods = data.filter_class;
        });
        this.statisticsPeriods = [
            'прогноз рік',
            this.todayYear,
            moment(new Date()).subtract(1, 'months').format('YYYY-MM'),
            moment(new Date()).format('YYYY-MM'),
            moment(new Date()).subtract(2, 'days').format('YYYY-MM-DD'),
            moment(new Date()).subtract(1, 'days').format('YYYY-MM-DD'),
            moment(new Date()).format('YYYY-MM-DD'),
        ];

        this.paymentFrom = this.fb.group({
            metod: [null, Validators.required],
            data_start: [null, Validators.required],
            data_end: [null, Validators.required],
            period: [null],
            id_order: null,
        });
        this.spendingForm = this.fb.group({
            data_start: [null, Validators.required],
            data_end: [null, Validators.required],
        });

        this.dataItems = this.fb.array([
            this.fb.group({
                data_payment: [null, Validators.required],
                metod_payment: ['iban', Validators.required],
                id_order: [null, Validators.required],
                id_payment: null,
                payment: [null, Validators.required],
                status: 'edit',
            }),
        ]);

        this.outlayData = this.fb.array([
            this.fb.group({
                data_outlay: [null, Validators.required],
                id_outlay_class: [null, Validators.required],
                id_outlay: null,
                money_outlay: [null, Validators.required],
                comment_outlay: [null, Validators.required],
                status: 'edit',
            }),
        ]);

        this.service.getPayments().subscribe((data: any) => {
            this.setDataPayments(data);
        });

        this.service.getOutlays().subscribe((data: any) => {
            this.setDataOutlay(data);
        });
    }

    removeEmptyValues(object) {
        const newObject = {
            ...object,
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

    setDataOutlay(data) {
        this.outlayData.clear();
        data.forEach((item: any) => {
            const dataOutlay = item.data_outlay.split('-');
            this.outlayData.push(
                this.fb.group({
                    data_outlay: [
                        { year: +dataOutlay[0], month: +dataOutlay[1], day: +dataOutlay[2] },
                        Validators.required,
                    ],
                    id_outlay: item.id_outlay,
                    id_outlay_class: [item.id_outlay_class, Validators.required],
                    money_outlay: [item.money_outlay, Validators.required],
                    comment_outlay: [item.comment_outlay, Validators.required],
                    status: 'edit',
                })
            );
        });

        this.outlayData.push(
            this.fb.group({
                data_outlay: [null, Validators.required],
                id_outlay: null,
                id_outlay_class: [null, Validators.required],
                money_outlay: [null, Validators.required],
                comment_outlay: [null, Validators.required],
                status: 'ok',
            })
        );
    }

    setDataPayments(data) {
        this.dataItems.clear();
        data.forEach((item, i) => {
            const dataArray = item.data_payment.split('-');

            this.dataItems.push(
                this.fb.group({
                    data_payment: [
                        { year: +dataArray[0], month: +dataArray[1], day: +dataArray[2] },
                        Validators.required,
                    ],
                    metod_payment: [item.metod_payment, Validators.required],
                    id_payment: [item.id_payment],
                    id_order: [item.id_order, Validators.required],
                    payment: [item.payment, Validators.required],
                    status: 'edit',
                })
            );
        });
        this.datePrevious = JSON.parse(localStorage.getItem('date_payment')) || null;
        this.dataItems.push(
            this.fb.group({
                data_payment: [this.datePrevious, Validators.required],
                metod_payment: ['iban', Validators.required],
                id_order: [null, Validators.required],
                id_payment: null,
                payment: [null, Validators.required],
                status: 'ok',
            })
        );
    }

    sendFiltersPayments() {
        let params;
        if (this.paymentFrom.value.id_order) {
            params = {
                id_order: this.paymentFrom.value.id_order,
            };
            this.service.getFilters(params, '/order_payments').subscribe((data: any) => {
                this.setDataPayments(data);
            });
        } else if (this.paymentFrom.value.period) {
            params = {
                data_start: this.editData(Object.values(this.paymentFrom.value.data_start)),
                data_end: this.editData(Object.values(this.paymentFrom.value.data_end)),
                iban: this.paymentFrom.value.metod === 'банк' || this.paymentFrom.value.metod === 'всі',
                cash: this.paymentFrom.value.metod === 'готівка' || this.paymentFrom.value.metod === 'всі',
                balans: this.paymentFrom.value.period,
            };

            this.service.getStaticPayments(params).subscribe((data: any) => {
                this.isShowStatistics = true;
                this.statisticsPayments = data;
                this.statisticsData = [];
            });
        } else {
            params = {
                data_start: this.editData(Object.values(this.paymentFrom.value.data_start)),
                data_end: this.editData(Object.values(this.paymentFrom.value.data_end)),
                iban: this.paymentFrom.value.metod === 'iban' || this.paymentFrom.value.metod === 'всі',
                cash: this.paymentFrom.value.metod === 'cash' || this.paymentFrom.value.metod === 'всі',
            };
            this.service.getFilters(params, '/payments').subscribe((data: any) => {
                this.setDataPayments(data);
            });
        }
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
    sendSpendingFilters() {
        const params = {
            data_start: this.editData(Object.values(this.spendingForm.value.data_start)),
            data_end: this.editData(Object.values(this.spendingForm.value.data_end)),
            outlay_search: 0,
        };
        this.service.getFilters(params).subscribe((data: any) => {
            this.setDataOutlay(data);
        });
    }

    actionClick(action, item, table = 'payment') {
        if (action === 'edit') {
            this.itemEdit = _.cloneDeep(item.value);
            item.patchValue({
                status: 'process',
            });
        } else if (action === 'close') {
            item.patchValue({
                ...this.itemEdit,
                status: 'edit',
            });
        } else if (action === 'edited') {
            if (table === 'outlay') {
                const params = {
                    data_outlay:
                        typeof item.value.data_outlay === 'string'
                            ? item.value.data_outlay
                            : this.editData(Object.values(item.value.data_outlay)),
                    id_outlay_class: item.value.id_outlay_class,
                    id_outlay: item.value.id_outlay,
                    money_outlay: +item.value.money_outlay,
                    comment_outlay: item.value.comment_outlay,
                };
                this.service.editOutlay(params).subscribe(() => {
                    item.patchValue({
                        status: 'edit',
                    });
                });
                return;
            }
            const params = {
                id_payment: +item.value.id_payment,
                data_payment:
                    typeof item.value.data_payment === 'string'
                        ? item.value.data_payment
                        : this.editData(Object.values(item.value.data_payment)),
                metod_payment: item.value.metod_payment,
                id_order: +item.value.id_order,
                payment: +item.value.payment,
            };

            this.service.editPayment(params).subscribe(() => {
                item.patchValue({
                    status: 'edit',
                });
            });
        } else if (action === 'ok') {
            localStorage.setItem('date_payment', JSON.stringify(this.dataItems.value.data_payment));
            this.dataItems.push(
                this.fb.group({
                    data_payment: [this.datePrevious, Validators.required],
                    metod_payment: 'iban',
                    id_payment: null,
                    id_order: [null, Validators.required],
                    payment: [null, Validators.required],
                    status: 'ok',
                })
            );
        }
    }

    savePayment() {
        const paymentForSave = this.dataItems.value[this.dataItems.value.length - 1];
        const params = {
            data_payment: this.editData(Object.values(paymentForSave.data_payment)),
            metod_payment: paymentForSave.metod_payment,
            id_order: +paymentForSave.id_order,
            payment: +paymentForSave.payment,
        };
        this.service.savePayment(params).subscribe(() => {
            this.dataItems.controls[this.dataItems.controls.length - 1].patchValue({
                status: 'edit',
            });
            this.datePrevious = paymentForSave.data_payment;
            this.dataItems.push(
                this.fb.group({
                    data_payment: [this.datePrevious, Validators.required],
                    metod_payment: 'iban',
                    id_payment: null,
                    id_order: [null, Validators.required],
                    payment: [null, Validators.required],
                    status: 'ok',
                })
            );
        });
    }

    saveOutlay() {
        const outlayForSave = this.outlayData.value[this.outlayData.value.length - 1];
        const params = {
            data_outlay: this.editData(Object.values(outlayForSave.data_outlay)),
            id_outlay_class: outlayForSave.id_outlay_class,
            money_outlay: +outlayForSave.money_outlay,
            comment_outlay: outlayForSave.comment_outlay,
        };

        this.service.saveOutlay(params).subscribe(() => {
            this.outlayData.controls[this.outlayData.controls.length - 1].patchValue({
                status: 'edit',
            });
            this.outlayData.push(
                this.fb.group({
                    data_outlay: [null, Validators.required],
                    id_outlay: null,
                    id_outlay_class: [null, Validators.required],
                    money_outlay: [null, Validators.required],
                    comment_outlay: [null, Validators.required],
                    status: 'ok',
                })
            );
        });
    }

    statisticsAtion() {
        if (!this.isShowStatistics) {
            this.service.getStatistics().subscribe((statistics) => {
                this.statisticsData = statistics;
                this.isShowStatistics = true;
            });
        } else {
            this.isShowStatistics = false;
            this.statisticsPayments = [];
        }
    }

    isEmptyObject(obj) {
        return !(obj && (Object.keys(obj).length === 0));
     }
}
