import { Component, OnInit } from '@angular/core';
import { UntypedFormArray, UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import * as _ from 'lodash';
import * as moment from 'moment';
import { forkJoin } from 'rxjs';
import { FinancesPageService } from '../services/finances.service';

@Component({
  selector: 'app-finances',
  templateUrl: './finances.component.html',
  styleUrls: ['./finances.component.sass'],
})
export class FinancesComponent implements OnInit {
  constructor(private _service: FinancesPageService, private _fb: UntypedFormBuilder) {}
  isShowSpinner = false;
  metodPayment = [];
  outlayClass: string[];
  paymentFrom: UntypedFormGroup;
  spendingForm;
  dataItems: UntypedFormArray;
  periods: string[];
  outlayData: UntypedFormArray;
  statisticsPeriods;
  statisticsData;
  isShowStatistics = false;
  statisticsPayments = [];
  itemEdit;
  datePrevious = {
    year: new Date().getFullYear(),
    month: new Date().getMonth(),
    day: new Date().getDay(),
  };

  datePreviousOutlay: any = {
    year: new Date().getFullYear(),
    month: +String(new Date().getMonth() + 1).padStart(2, '0'),
    day: +String(new Date().getDate()).padStart(2, '0'),
  };
  todayYear = new Date().getFullYear();
  alert = {
    type: '',
    message: '',
    isShow: false,
  };
  ngOnInit(): void {
    this.statisticsPeriods = [
      'прогноз рік',
      this.todayYear,
      moment(new Date()).subtract(1, 'months').format('YYYY-MM'),
      moment(new Date()).format('YYYY-MM'),
      moment(new Date()).subtract(2, 'days').format('YYYY-MM-DD'),
      moment(new Date()).subtract(1, 'days').format('YYYY-MM-DD'),
      moment(new Date()).format('YYYY-MM-DD'),
    ];

    this.paymentFrom = this._fb.group({
      metod: [null, Validators.required],
      data_start: [null, Validators.required],
      data_end: [null, Validators.required],
      period: [null],
      id_order: null,
    });
    this.spendingForm = this._fb.group({
      data_start: [null, Validators.required],
      data_end: [null, Validators.required],
    });

    this.dataItems = this._fb.array([
      this._fb.group({
        data_payment: [this.datePrevious, Validators.required],
        metod_payment: ['iban', Validators.required],
        id_order: [null, Validators.required],
        id_payment: null,
        payment: [null, Validators.required],
        status: 'edit',
      }),
    ]);

    this.outlayData = this._fb.array([
      this._fb.group({
        data_outlay: [null, Validators.required],
        id_outlay_class: [null, Validators.required],
        id_outlay: null,
        money_outlay: [null, Validators.required],
        comment_outlay: [null, Validators.required],
        status: 'edit',
      }),
    ]);

    this.isShowSpinner = true;
    forkJoin([this._service.getMethods(), this._service.getPayments(), this._service.getOutlays()]).subscribe(
      (data: any[]) => {
        this.metodPayment = data[0].metod_payment;
        this.outlayClass = data[0].outlay_class;
        this.periods = data[0].filter_class;
        this.setDataPayments(data[1]);
        this.setDataOutlay(data[2]);
        this.isShowSpinner = false;
      },
      () => {
        this.isShowSpinner = false;
      }
    );
  }

  removeEmptyValues(object) {
    const newObject = {
      ...object,
    };
    for (const key in newObject) {
      if (newObject.hasOwnProperty(key)) {
        const value = newObject[key];
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
        this._fb.group({
          data_outlay: [{ year: +dataOutlay[0], month: +dataOutlay[1], day: +dataOutlay[2] }, Validators.required],
          id_outlay: item.id_outlay,
          id_outlay_class: [item.id_outlay_class, Validators.required],
          money_outlay: [item.money_outlay, Validators.required],
          comment_outlay: [item.comment_outlay, Validators.required],
          status: 'edit',
        })
      );
    });

    this.outlayData.push(
      this._fb.group({
        data_outlay: [this.datePreviousOutlay, Validators.required],
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
    data.forEach((item) => {
      const dataArray = item.data_payment.split('-');
      this.dataItems.push(
        this._fb.group({
          data_payment: [{ year: +dataArray[0], month: +dataArray[1], day: +dataArray[2] }, Validators.required],
          metod_payment: [item.metod_payment, Validators.required],
          id_payment: [item.id_payment],
          id_order: [item.id_order, Validators.required],
          payment: [item.payment, Validators.required],
          status: 'edit',
        })
      );
    });
    this.datePrevious = JSON.parse(localStorage.getItem('date_payment')) || {
      year: new Date().getFullYear(),
      month: +String(new Date().getMonth() + 1).padStart(2, '0'),
      day: +String(new Date().getDate()).padStart(2, '0'),
    };
    this.dataItems.push(
      this._fb.group({
        data_payment: [this.datePrevious, Validators.required],
        metod_payment: ['iban', Validators.required],
        id_order: [null, Validators.required],
        id_payment: null,
        payment: [null, Validators.required],
        status: 'ok',
      })
    );
  }

  requestIncorrect() {
    this.isShowSpinner = false;
    this.alert = {
      isShow: true,
      type: 'danger',
      message: 'Уппс, щось пішло не так',
    };
    setTimeout(() => {
      this.alertChange(false);
    }, 3000);
  }

  sendFiltersPayments() {
    let params;
    if (this.paymentFrom.value.id_order) {
      params = {
        id_order: this.paymentFrom.value.id_order,
      };
      this.isShowSpinner = true;
      this._service.getFilters(params, '/order_payments').subscribe(
        (data: any) => {
          this.setDataPayments(data);
          this.isShowSpinner = false;
        },
        () => {
          this.requestIncorrect();
        }
      );
    } else if (this.paymentFrom.value.period) {
      params = {
        data_start: this.editData(Object.values(this.paymentFrom.value.data_start)),
        data_end: this.editData(Object.values(this.paymentFrom.value.data_end)),
        iban: this.paymentFrom.value.metod === 'банк' || this.paymentFrom.value.metod === 'всі',
        cash: this.paymentFrom.value.metod === 'готівка' || this.paymentFrom.value.metod === 'всі',
        balans: this.paymentFrom.value.period,
      };
      this.isShowSpinner = true;
      this._service.getStaticPayments(params).subscribe(
        (data: any) => {
          this.isShowStatistics = true;
          this.statisticsPayments = data;
          this.statisticsData = [];
          this.isShowSpinner = false;
        },
        () => {
          this.requestIncorrect();
        }
      );
    } else {
      params = {
        data_start: this.editData(Object.values(this.paymentFrom.value.data_start)),
        data_end: this.editData(Object.values(this.paymentFrom.value.data_end)),
        iban: this.paymentFrom.value.metod === 'iban' || this.paymentFrom.value.metod === 'всі',
        cash: this.paymentFrom.value.metod === 'cash' || this.paymentFrom.value.metod === 'всі',
      };
      this.isShowSpinner = true;
      this._service.getFilters(params, '/payments').subscribe(
        (data: any) => {
          this.setDataPayments(data);
          this.isShowSpinner = false;
        },
        () => {
          this.requestIncorrect();
        }
      );
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
    this.isShowSpinner = true;
    this._service.getFilters(params).subscribe(
      (data: any) => {
        this.setDataOutlay(data);
        this.isShowSpinner = false;
      },
      () => {
        this.requestIncorrect();
      }
    );
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
            typeof item.value.data_outlay === 'string' ? item.value.data_outlay : this.editData(Object.values(item.value.data_outlay)),
          id_outlay_class: item.value.id_outlay_class,
          id_outlay: item.value.id_outlay,
          money_outlay: +item.value.money_outlay,
          comment_outlay: item.value.comment_outlay,
        };
        this._service.editOutlay(params).subscribe(() => {
          item.patchValue({
            status: 'edit',
          });
          this.alert = {
            isShow: true,
            type: 'success',
            message: 'Збережено',
          };
          setTimeout(() => {
            this.alertChange(false);
          }, 3000);
        });
        return;
      }
      const params = {
        id_payment: +item.value.id_payment,
        data_payment:
          typeof item.value.data_payment === 'string' ? item.value.data_payment : this.editData(Object.values(item.value.data_payment)),
        metod_payment: item.value.metod_payment,
        id_order: +item.value.id_order,
        payment: +item.value.payment,
      };

      this._service.editPayment(params).subscribe(() => {
        item.patchValue({
          status: 'edit',
        });
        this.alert = {
          isShow: true,
          type: 'success',
          message: 'Збережено',
        };
        setTimeout(() => {
          this.alertChange(false);
        }, 3000);
      });
    } else if (action === 'ok') {
      localStorage.setItem('date_payment', JSON.stringify(this.dataItems.value.data_payment));
      this.dataItems.push(
        this._fb.group({
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
    this.isShowSpinner = true;
    this._service.savePayment(params).subscribe(
      () => {
        this.dataItems.controls[this.dataItems.controls.length - 1].patchValue({
          status: 'edit',
        });
        this.datePrevious = paymentForSave.data_payment;
        this.dataItems.push(
          this._fb.group({
            data_payment: [this.datePrevious, Validators.required],
            metod_payment: 'iban',
            id_payment: null,
            id_order: [null, Validators.required],
            payment: [null, Validators.required],
            status: 'ok',
          })
        );
        this.isShowSpinner = false;
        this.alert = {
          isShow: true,
          type: 'success',
          message: 'Збережено',
        };
        setTimeout(() => {
          this.alertChange(false);
        }, 3000);
      },
      () => {
        this.requestIncorrect();
      }
    );
  }

  saveOutlay() {
    const outlayForSave = this.outlayData.value[this.outlayData.value.length - 1];
    const params = {
      data_outlay: this.editData(Object.values(outlayForSave.data_outlay)),
      id_outlay_class: outlayForSave.id_outlay_class,
      money_outlay: +outlayForSave.money_outlay,
      comment_outlay: outlayForSave.comment_outlay,
    };

    this.datePreviousOutlay = outlayForSave.data_outlay;
    this.isShowSpinner = true;
    this._service.saveOutlay(params).subscribe(
      () => {
        this.isShowSpinner = false;
        this.outlayData.controls[this.outlayData.controls.length - 1].patchValue({
          status: 'edit',
        });
        this.outlayData.push(
          this._fb.group({
            data_outlay: [this.datePreviousOutlay, Validators.required],
            id_outlay: null,
            id_outlay_class: [null, Validators.required],
            money_outlay: [null, Validators.required],
            comment_outlay: [null, Validators.required],
            status: 'ok',
          })
        );
        this.alert = {
          isShow: true,
          type: 'success',
          message: 'Збережено',
        };
        setTimeout(() => {
          this.alertChange(false);
        }, 3000);
      },
      () => {
        this.requestIncorrect();
      }
    );
  }

  statisticsAtion() {
    if (!this.isShowStatistics) {
      this.isShowSpinner = true;
      this._service.getStatistics().subscribe((statistics) => {
        this.statisticsData = statistics;
        this.isShowStatistics = true;
        this.isShowSpinner = false;
      });
    } else {
      this.isShowStatistics = false;
      this.statisticsPayments = [];
    }
  }

  isEmptyObject(obj) {
    return !(obj && Object.keys(obj).length === 0);
  }

  alertChange(e) {
    this.alert.isShow = e;
  }
}
