import { Component, OnInit, TemplateRef } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { NgbOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import * as _ from 'lodash';
import * as moment from 'moment';
import { DataAutofillInterface } from '../interfaces/autofill-data';
import { MainPageService } from '../services/main-table.service';
import { UsefulService } from '../services/useful.service';
import { DataAutofill } from '../utils/autofill';

@Component({
  selector: 'app-main-table',
  templateUrl: './main-table.component.html',
  styleUrls: ['./main-table.component.sass'],
})
export class MainTableComponent implements OnInit {
  orders = [];
  isShowSpinner = false;
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
  additionalNumber: number = 0;
  filtersForm: FormGroup;
  fulfilledOrderItems = [
    { id: 1, value: true, name: 'виконані' },
    { id: 2, value: 'all', name: 'всі' },
    { id: 3, value: false, name: 'не виконані' },
  ];
  dataFilters = [];

  constructor(
    private _service: MainPageService,
    private _offcanvasService: NgbOffcanvas,
    private _fb: FormBuilder,
    private _generalService: UsefulService
  ) {}

  ngOnInit(): void {
    this.getAllData();
    this.initForm();
  }

  initForm() {
    this.filtersForm = this._fb.group({
      dataStart: null,
      dataEnd: null,
      fulfilled: 'all',
      phone_client: null,
      id_client: null,
      team: null,
      city: null,
      coach: null,
      kod_model: null,
      kod_model_like: null,
      kolor_model_like: null,
    });
  }

  changeFiled(event, fieldSend: string) {
    if (event.term.length >= DataAutofill[fieldSend]) {
      this._generalService.getAutofill({ [fieldSend]: event.term }).subscribe((data: DataAutofillInterface[]) => {
        this.dataFilters = data;
      });
    }
  }

  clearFilterData() {
    this.dataFilters = [];
  }

  resetFilters() {
    this.filtersForm.reset();
    this.filtersForm.patchValue({
      fulfilled: 'all',
    });
  }

  applyFilters() {
    this.isShowSpinner = true;
    this._service.sendFilters(this.cleanObject(_.cloneDeep(this.filtersForm.value))).subscribe(
      (data: any) => {
        this.orders = data;
        this.isShowSpinner = false;
        this.closeFilterMenu();
      },
      () => {
        this.isShowSpinner = false;
        this.closeFilterMenu();
      }
    );
  }

  cleanObject(obj) {
    for (var propName in obj) {
      if (obj[propName] === null || obj[propName] === undefined) {
        delete obj[propName];
      } else if (propName === 'dataEnd') {
        obj.data_end = this.editData(obj[propName]);
        delete obj[propName];
      } else if (propName === 'dataStart') {
        obj.data_start = this.editData(obj[propName]);
        delete obj[propName];
      }
    }
    return obj;
  }

  editData(data) {
    data = Object.values(data);
    return data
      .map((item) => {
        if (item <= 9) {
          return '0' + item;
        }
        return item;
      })
      .join('-');
  }

  openFilterMenu(content: TemplateRef<any>) {
    this.isShowFilter = true;
    this._offcanvasService.open(content, { position: 'top' });
  }

  closeFilterMenu() {
    this.isShowFilter = false;
    this._offcanvasService.dismiss();
    this.resetFilters();
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
    if (event && event.type === 'click') {
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
    if (event && event.type === 'click') {
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

  showAlertsForPhase(isOkay = true) {
    this.alert = {
      isShow: true,
      type: isOkay ? 'success' : 'danger',
      message: isOkay ? 'Дані змінено' : 'Дані не збігаються',
    };
    setTimeout(() => {
      this.alertChange(false);
    }, 3000);
  }

  sendPhases(order, phaseIndex, phase, event, item) {
    const params = [...order[phase]];
    params[phaseIndex] = item - event.target.value;

    this._service.sendPhase(order.id_order, { [phase]: params }).subscribe((data: any) => {
      this.showMessage(data.message);
      this.orders = this.orders.map((orderItem) => {
        if (orderItem.id_order === order.id_order) {
          orderItem = {
            ...orderItem,
            [phase]: [...params],
          };
        }
        return orderItem;
      });

      setTimeout(() => {
        this.alertChange(false);
      }, 3000);
    });
  }

  sendPhase(item, phase, e) {
    const params = {
      [phase]: [item[phase] - e.target.value],
    };

    this._service.sendPhase(item.id_order, params).subscribe((data: any) => {
      this.showMessage(data.message);
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

      setTimeout(() => {
        this.alertChange(false);
      }, 3000);
    });
  }

  getAllData() {
    this.isShowSpinner = true;
    this._service.getListMain().subscribe(
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
        sum += Array.isArray(item[phase]) ? item[phase].reduce((partialSum, a) => partialSum + a, 0) : item[phase];
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
    return '';
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
      order.address,
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
        sum += Array.isArray(item.phase_1) ? item.phase_1.reduce((partialSum, a) => partialSum + a, 0) : item.phase_1;
      }
    });
    this.queue = sum / 2;
    return this.queue;
  }

  makeDone(id, fulfilledOrder, i) {
    this._service.changeFulfilled(id, { status_order: fulfilledOrder }).subscribe((data: any) => {
      this.orders.forEach((order, index) => {
        if (i === index) {
          order.fulfilled_order = !order.fulfilled_order;
        }
      });
      this.showMessage(data.message);
    });
  }

  changeSpeed() {
    const days = Math.ceil((this.queue + this.additionalNumber) / this.speed);
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

  showMessage(message) {
    this.alert = {
      isShow: true,
      type: 'success',
      message: message,
    };
    setTimeout(() => {
      this.alertChange(false);
    }, 3000);
  }

  alertChange(e) {
    this.alert.isShow = e;
  }
}
