import { Component, Input, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import locale from 'date-fns/locale/en-US';
import * as moment from 'moment';
import { DatepickerOptions } from 'ng2-datepicker';
import { tap } from 'rxjs';
import { modelsData } from 'src/assets/models-data/modelsData';
import { formatNumber } from 'src/common/common';
import { DataAutofill } from '../client-form/autofill';
import { ClientService } from '../services/client.service';
import { MainPageService } from '../services/main-table.service';
import { CreateOrderService } from '../services/orders.service';
import { ProductsService } from '../services/products.service';
import { UsefulService } from '../services/useful.service';
@Component({
  selector: 'app-create-order',
  templateUrl: './create-order.component.html',
  styleUrls: ['./create-order.component.sass'],
})
export class CreateOrderComponent implements OnInit {
  constructor(
    private _fb: FormBuilder,
    private _service: CreateOrderService,
    private _route: ActivatedRoute,
    private _serviceMain: MainPageService,
    private _clientService: ClientService,
    private _productService: ProductsService,
    private _usefulService: UsefulService
  ) {}

  @Input() isNew: Boolean = true;
  displayMonths = 2;
  isShowSpinner = false;
  model: NgbDateStruct;
  navigation = 'select';
  showWeekNumbers = false;
  outsideDays = 'visible';

  isEditClient = false;
  orderForm: FormArray;
  clientForm: FormGroup;
  isGetPostR: Boolean = false;
  recipientForm: FormGroup;
  priceAll: FormGroup;
  idOrder = 0;
  isSaveClient: Boolean = false;
  isSaveRecipient: Boolean;
  fulfilledOrder: Boolean = false;
  options: DatepickerOptions = {
    minDate: new Date(''),
    format: 'yyyy-MM-dd',
    formatDays: 'EEEEE',
    firstCalendarDay: 1,
    locale,
    position: 'bottom',
    placeholder: 'dd.mm.yyyy',
    calendarClass: 'datepicker-default',
    scrollBarColor: '#dfe3e9',
  };

  orders = [];

  todayYear = new Date().getFullYear();
  dateToday = null;
  dataPlaneOrder = null;
  dateForms: FormGroup;
  isRecipient = false;
  kodItems;
  materialsItems;
  clientDataItems = [];
  coachDataItems;
  infoForSave: any;
  commentOrder = null;
  discount = 0;
  doneOrder: Boolean = false;
  alert = {
    type: '',
    message: '',
    isShow: false,
  };
  ngOnInit(): void {
    this.init();
    this.viewChanges();
    this.dataPlaneOrder = JSON.parse(localStorage.getItem('date_plane_send')) || null;
    this.dateToday = JSON.parse(localStorage.getItem('dateToday')) || null;
    if (this._route.snapshot.params.id) {
      this.idOrder = +this._route.snapshot.params.id;
      this.getOrder();
    }
  }

  requiredFalse() {
    return (control) => {
      return control.value;
    };
  }

  init() {
    this.commentOrder = null;
    this.isSaveClient = false;
    this.isSaveRecipient = false;
    this.dateForms = this._fb.group({
      date_create: moment().format('YYYY-MM-DD'),
      date_plane_send: null,
      data_send_order: null,
    });

    this.priceAll = this._fb.group({
      sum_payment: 0,
      real_money: 0,
      different: 0,
    });

    this.orderForm = this._fb.array([
      this._fb.group({
        article: null,
        id_product: null,
        colors: null,
        id_color_1: null,
        color_name_1: null,
        part_1: null,
        id_color_2: null,
        color_name_2: null,
        part_2: null,
        id_color_3: null,
        color_name_3: null,
        part_3: null,
        id_color_4: null,
        color_name_4: null,
        part_4: null,
        price: null,
        qty_pars: [null, Validators.required],
        phase_1: 0,
        phase_2: 0,
        phase_3: 0,
        phase_1_default: 0,
        phase_2_default: 0,
        phase_3_default: 0,
        qty_pars_default: null,
        sum_pars: null,
        comment: null,
        isNew: [true, this.requiredFalse()],
        isChange: false,
      }),
    ]);

    this.clientForm = this._fb.group({
      id_client: null,
      phone: [null, Validators.required],
      second_name: [null, Validators.required],
      first_name: [null, Validators.required],
      surname: null,
      city: [null, Validators.required],
      np_number: [null, Validators.required],
      team: null,
      coach: null,
      zip_code: null,
      address: null,
      comment: null,
    });

    this.recipientForm = this._fb.group({
      id_client: null,
      phone: [null, Validators.required],
      second_name: [null, Validators.required],
      first_name: [null, Validators.required],
      surname: null,
      city: [null, Validators.required],
      np_number: [null, Validators.required],
      team: null,
      zip_code: null,
      address: null,
      comment: null,
    });
  }

  sumAll(isCountDiscount = true) {
    const sumAllItems = [];

    this.priceAll.patchValue({
      sum_payment: 0,
    });
    this.orderForm.controls.map((order) => {
      this.priceAll.patchValue({
        sum_payment: this.priceAll.value.sum_payment + order.value.sum_pars,
      });
    });
    if (isCountDiscount) {
      sumAllItems.push(this.priceAll.value.sum_payment - this.discount, this.priceAll.value.real_money, this.priceAll.value.different);
    } else {
      sumAllItems.push(this.priceAll.value.sum_payment, this.priceAll.value.real_money, this.priceAll.value.different);
    }
    return sumAllItems.join(' / ');
  }

  viewChanges() {
    this.orderForm.controls.map((order) => {
      order
        .get('qty_pars')
        .valueChanges.pipe(
          tap((data) => {
            const type = modelsData[order.value.article?.substring(0, 3)] || modelsData[order.value.article?.substring(0, 2)] || '';

            order.patchValue({
              sum_pars: data * order.value.price,
              phase_1: type.includes('брелок') ? +data : +(data * 2),
              phase_2: type.includes('брелок') ? +data : +(data * 2),
              phase_3: +data,
            });
          })
        )
        .subscribe();
      order
        .get('price')
        .valueChanges.pipe(
          tap((data) => {
            if (order.value.isNew) {
              order.patchValue({
                sum_pars: data * order.value.qty_pars,
                isNew: true,
                isChange: false,
              });
            } else if (!order.value.isNew) {
              order.patchValue({
                sum_pars: data * order.value.qty_pars,
                isNew: false,
                isChange: true,
              });
            }
          })
        )
        .subscribe();

      order.get('comment').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });
      order.get('id_color_1').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });

      order.get('id_color_2').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });

      order.get('id_color_3').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });

      order.get('id_color_4').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });

      order.get('article').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });

      order.get('colors').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });

      order.get('part_1').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });

      order.get('part_2').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });

      order.get('part_3').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });

      order.get('part_4').valueChanges.subscribe(() => {
        this.changeStatusProduct(order);
      });
    });

    this.clientForm.valueChanges.subscribe(() => {
      if (this.isSaveClient) {
        this.isEditClient = true;
      }
    });
  }

  changeStatusProduct(product) {
    if (product.value.isNew) {
      product.patchValue({
        isNew: true,
        isChange: false,
      });
    } else if (!product.value.isNew) {
      product.patchValue({
        isNew: false,
        isChange: true,
      });
    }
  }

  changeMaterial(value, field = 'name_material', isKode = false) {
    if (value.length >= DataAutofill[field]) {
      this._usefulService.getAutofill({ [field]: value }).subscribe((data: any) => {
        !isKode ? (this.materialsItems = data) : (this.kodItems = data);
      });
    } else {
      this.materialsItems = [];
      this.kodItems = [];
    }
  }

  chooseKode(value, index) {
    if (value && value.hasOwnProperty('id_product')) {
      this.orderForm.controls.map((order, ind) => {
        this._productService.getProduct(value.id_product).subscribe((data: any) => {
          if (index === ind && Object.keys(data).length) {
            order.patchValue(
              {
                id_product: data.id_product,
                article: data.article,
                colors: data.colors,
                color_name_1: data.color_name_1 || null,
                part_1: data.part_1,
                id_color_1: data.id_color_1,
                id_color_2: data.id_color_2,
                id_color_3: data.id_color_3,
                id_color_4: data.id_color_4,
                color_name_2: data.color_name_2 || null,
                part_2: data.part_2,
                color_name_3: data.color_name_3 || null,
                part_3: data.part_3,
                color_name_4: data.color_name_4 || null,
                part_4: data.part_4,
                price: data.price,
                comment: data.comment,
                isNew: false,
                isChange: false,
              },
              { emitEvent: false }
            );
          }
        });
      });
    } else {
      console.log('else', value, index);
      this.orderForm.controls.map((order) => {
        order.patchValue({
          article: value.value,
        });
      });
    }
    this.kodItems = [];
  }

  changeIdColor(order, field, value) {
    if (value && value.hasOwnProperty('id_material')) {
      order.patchValue({
        [field]: value.id_material,
      });
    }
    this.resetMaterialsItems();
  }

  resetMaterialsItems() {
    this.materialsItems = [];
  }

  changeCoach(form, field) {
    if (form.value[field] === form.value.second_name) {
      form.patchValue({
        [field]: null,
      });
    } else {
      form.patchValue({
        [field]: form.value.second_name,
      });
    }
  }

  addOrder() {
    this.orderForm.push(
      this._fb.group({
        article: null,
        id_product: null,
        colors: null,
        id_color_1: null,
        color_name_1: null,
        color_name_2: null,
        color_name_3: null,
        color_name_4: null,
        part_1: null,
        id_color_2: null,
        part_2: null,
        id_color_3: null,
        part_3: null,
        id_color_4: null,
        part_4: null,
        price: null,
        qty_pars: [null, Validators.required],
        phase_1: 0,
        phase_2: 0,
        phase_3: 0,
        phase_1_default: 0,
        phase_2_default: 0,
        phase_3_default: 0,
        qty_pars_default: null,
        sum_pars: null,
        comment: null,
        isNew: [true, this.requiredFalse()],
        isChange: false,
      })
    );
    this.viewChanges();
  }

  deleteOrder(index) {
    this.orderForm.controls.splice(index, 1);
    this.orderForm.value.splice(index, 1);
  }

  saveProduct(index, order) {
    const params = {
      article: order.value.article || 0,
      id_color_1: order.value.id_color_1 || null,
      part_1: +order.value.part_1 || null,
      id_color_2: +order.value.id_color_2 || null,
      part_2: +order.value.part_2 || null,
      id_color_3: +order.value.id_color_3 || null,
      part_3: +order.value.part_3 || null,
      id_color_4: +order.value.id_color_4 || null,
      part_4: +order.value.part_4 || null,
      price: +order.value.price || 0,
      comment: order.value.comment,
      colors: order.value.colors || null,
    };
    this.isShowSpinner = true;

    this._productService.saveProduct(params).subscribe(
      (data: any) => {
        order.patchValue({
          isNew: false,
          id_product: data.id_product,
        });
        this.isShowSpinner = false;
      },
      () => {
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
    );
  }

  editProduct(order) {
    const params = {
      article: order.value.article || 0,
      id_color_1: order.value.id_color_1 || null,
      part_1: +order.value.part_1 || null,
      id_color_2: +order.value.id_color_2 || null,
      part_2: +order.value.part_2 || null,
      id_color_3: +order.value.id_color_3 || null,
      part_3: +order.value.part_3 || null,
      id_color_4: +order.value.id_color_4 || null,
      part_4: +order.value.part_4 || null,
      price: +order.value.price || 0,
      comment: order.value.comment,
      colors: order.value.colors || 0,
    };
    this.isShowSpinner = true;

    this._productService.editProduct(order.value.id_product, params).subscribe(
      (data: any) => {
        order.patchValue({
          isNew: false,
          id_product: data.id_product,
          isChange: false,
        });
        this.isShowSpinner = false;
      },
      () => {
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
    );
  }

  clearDataClient() {
    this.clientDataItems = [];
  }

  getParamsClient() {
    return {
      phone: this.clientForm.value.phone,
      second_name: this.clientForm.value.second_name,
      first_name: this.clientForm.value.first_name,
      surname: this.clientForm.value.surname,
      np_number: this.clientForm.value.np_number,
      team: this.clientForm.value.team,
      coach: this.clientForm.value.coach,
      zip_code: +this.clientForm.value.zip_code,
      address: this.clientForm.value.address,
      comment: this.clientForm.value.comment,
      city: this.clientForm.value.city,
    };
  }
  saveClient(form = this.clientForm, params: any = this.getParamsClient()) {
    this.isShowSpinner = true;
    this._clientService.saveClient(params).subscribe(
      (data: any) => {
        this.isShowSpinner = false;
        form.patchValue({
          id_client: data.id_client,
        });
        this.alert = {
          isShow: true,
          type: 'success',
          message: 'Дані збережено',
        };
        setTimeout(() => {
          this.alertChange(false);
        }, 3000);
        this.isSaveClient = true;
        // this.isSaveRecipient = true;
      },
      (error) => {
        const key = Object.keys(error.error);
        if (key[0] === 'coach') {
          this.clientForm.controls.coach.setErrors({
            message: Object.values(error.error)[0],
          });
        } else {
          form.controls[key[0]].setErrors({
            message: Object.values(error.error)[0],
          });
        }
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
    );
  }

  getParamsRecipient() {
    return {
      phone: this.recipientForm.value.phone,
      second_name: this.recipientForm.value.second_name,
      first_name: this.recipientForm.value.first_name,
      surname: this.recipientForm.value.surname,
      np_number: +this.recipientForm.value.np_number,
      id_team: this.recipientForm.value.id_team,
      coach: this.clientForm.value.coach,
      team: this.recipientForm.value.team,
      zip_code: +this.recipientForm.value.zip_code,
      address: this.recipientForm.value.address,
      comment: this.recipientForm.value.comment,
      city: this.recipientForm.value.city,
    };
  }
  saveRecipient() {
    this.saveClient(this.recipientForm, this.getParamsRecipient());
  }

  saveForm(event) {
    this.isSaveClient = true;
    if (event.isNew) {
      if (event.isClient) {
        this.saveClient();
      } else if (!event.isClient) {
        this.saveRecipient();
      }
    } else {
      const params = event.isClient ? this.getParamsClient() : this.getParamsClient();
      const form: FormGroup = event.isClient ? this.clientForm : this.recipientForm;
      this.editClient(form, params);
    }
  }

  editClient(form, params) {
    this._clientService.editClient(params, form.value.id_client).subscribe(
      (data: any) => {
        this.isSaveClient = 1 as any;
        this.isSaveRecipient = 1 as any;
        this.isShowSpinner = false;
        form.patchValue({
          id_client: data.id_recipient || form.value.id_client,
        });
        this.alert = {
          isShow: true,
          type: 'success',
          message: 'Дані збережено',
        };
        setTimeout(() => {
          this.alertChange(false);
        }, 3000);
      },
      (error) => {
        const key = Object.keys(error.error);
        form.controls[key[0]].setErrors({
          message: Object.values(error.error)[0],
        });
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
    );
  }

  makeArrayDataOrder(key) {
    const result = [];
    if (this.orderForm.value[0][key] !== undefined) {
      this.orderForm.value.map((order) => {
        result.push(+order[key] || 0);
      });
    }
    return result;
  }

  rewriteData(data) {
    if (this.isEmptyObject(data)) {
      return null;
    }
    const month = +data.month < 10 ? '0' + data.month : data.month;
    const day = +data.day < 10 ? '0' + data.day : data.day;

    return data ? [data.year, month, day].join('-') : null;
  }

  saveAll(mode = 'create') {
    console.log(this.clientForm.value);

    const params = {
      date_create: this.rewriteData(this.dateToday),
      id_client: this.clientForm.value.id_client,
      id_recipient: !this.isRecipient ? this.clientForm.value.id_client : this.recipientForm.value.id_client, // (2 або ід_клієнт)
      id_models: this.makeArrayDataOrder('id_product'),
      price_model_sell: this.makeArrayDataOrder('price'),
      qty_pars: this.makeArrayDataOrder('qty_pars'),
      phase_1: this.makeArrayDataOrder('phase_1'),
      phase_2: this.makeArrayDataOrder('phase_2'),
      phase_3: this.makeArrayDataOrder('phase_3'),
      date_plane_send: this.rewriteData(this.dataPlaneOrder), // - прогнозована
      discount: +this.discount,
      sum_payment: +this.sumAll(false).split('/')[0].trim(),
      status_order: false,
      comment: this.commentOrder,
    };

    if (mode === 'edit') {
      this._service.editOrder(params, +this.idOrder).subscribe((data: any) => {
        this.idOrder = +data.id_order || this.idOrder;
        // this.doneOrder = true;
        localStorage.setItem('date_plane_send', JSON.stringify(this.dataPlaneOrder));
        localStorage.setItem('dateToday', JSON.stringify(this.dateToday));
        this.alert = {
          isShow: true,
          type: 'success',
          message: 'Дані збережено',
        };
        setTimeout(() => {
          this.alertChange(false);
        }, 3000);
      });
    } else {
      this._service.saveOrder(params).subscribe((data: any) => {
        this.idOrder = +data.id_order || this.idOrder;
        this.doneOrder = true;
        this.isNew = false;
        localStorage.setItem('date_plane_send', JSON.stringify(this.dataPlaneOrder));
        localStorage.setItem('dateToday', JSON.stringify(this.dateToday));
        this.alert = {
          isShow: true,
          type: 'success',
          message: 'Дані збережено',
        };
        setTimeout(() => {
          this.alertChange(false);
        }, 3000);
      });
    }
  }

  setClientData(dataClient) {
    this.clientForm.setValue(
      {
        coach: dataClient?.coach,
        comment: dataClient.comment,
        first_name: dataClient.first_name,
        id_client: dataClient.id_client,
        team: dataClient.team,
        phone: dataClient.phone,
        second_name: dataClient.second_name,
        city: dataClient.city,
        address: dataClient.address,
        surname: dataClient.surname,
        zip_code: dataClient.zip_code,
        np_number: dataClient.np_number,
      },
      { emitEvent: false }
    );
    this.isSaveClient = true;
    this.viewChanges();
  }

  showRecipient() {
    this.isRecipient = !this.isRecipient;
  }
  setRecipientData(dataRecipient) {
    this.recipientForm.setValue(
      {
        comment: dataRecipient.comment,
        first_name: dataRecipient.first_name,
        id_client: dataRecipient.id_client,
        team: dataRecipient.team,
        phone: dataRecipient.phone,
        second_name: dataRecipient.second_name,
        city: dataRecipient.city,
        address: dataRecipient.address,
        surname: dataRecipient.surname,
        zip_code: dataRecipient.zip_code,
        np_number: dataRecipient.np_number,
      },
      { emitEvent: false }
    );

    this.isSaveRecipient = true;
    this.viewChanges();
  }

  getOrder() {
    this.isShowSpinner = true;
    this._service
      .getOrder(this.idOrder)
      .pipe(
        tap(() => {
          this.isShowSpinner = true;
        })
      )
      .subscribe((data: any) => {
        if (Object.keys(data).length) {
          const arrDataOrder = data.date_create.split('-');
          const arrDataPlane = data.date_plane_send.split('-');
          this.commentOrder = data.comment;
          this.dateToday = { year: +arrDataOrder[0], month: +arrDataOrder[1], day: +arrDataOrder[2] };
          this.dataPlaneOrder = { year: +arrDataPlane[0], month: +arrDataPlane[1], day: +arrDataPlane[2] };
          this.discount = data.discount;
          this.fulfilledOrder = data.status_order;
          this._clientService.getClient(data.id_client).subscribe((dataClient: any) => {
            this.isShowSpinner = false;
            this.setClientData(dataClient);
            if (data.id_client !== data.id_recipient) {
              this.isRecipient = true;
              this._clientService.getClient(data.id_recipient).subscribe((dataRecipient: any) => {
                this.setRecipientData(dataRecipient);
              });
            }
            this.getModels(data);
          });

          this.priceAll.patchValue({
            sum_payment: data.sum_payment,
          });
          this.isNew = false;
        } else {
          this.init();
          this.viewChanges();
          this.isNew = true;
          this.dataPlaneOrder = null;
          this.isShowSpinner = false;
          this.alert = {
            isShow: true,
            type: 'warning',
            message: 'Користувача не знайдено',
          };
          setTimeout(() => {
            this.alertChange(false);
          }, 3000);
        }
      });
  }
  getModels(data) {
    data.id_models.forEach((idModel, index) => {
      if (index === 0) {
        this.orderForm.clear();
      }

      this._productService.getProduct(idModel).subscribe((dataModel: any) => {
        this.orderForm.push(
          this._fb.group({
            id_product: dataModel.id_product,
            article: dataModel.article,
            colors: dataModel.colors,
            color_name_1: dataModel.color_name_1 || null,
            part_1: dataModel.part_1,
            id_color_1: dataModel.id_color_1,
            id_color_2: dataModel.id_color_2,
            id_color_3: dataModel.id_color_3,
            id_color_4: dataModel.id_color_4,
            color_name_2: dataModel.color_name_2 || null,
            part_2: dataModel.part_2,
            color_name_3: dataModel.color_name_3 || null,
            part_3: dataModel.part_3,
            color_name_4: dataModel.color_name_4 || null,
            part_4: dataModel.part_4,
            price: data.price_model_sell[index],
            phase_1: data.phase_1[index],
            phase_2: data.phase_2[index],
            phase_3: data.phase_3[index],
            phase_1_default: data.phase_1[index],
            phase_2_default: data.phase_2[index],
            phase_3_default: data.phase_3[index],
            comment: dataModel.comment,
            qty_pars: [data.qty_pars[index], Validators.required],
            qty_pars_default: data.qty_pars[index],
            sum_pars: data.qty_pars[index] * data.price_model_sell[index],
            isNew: false,
            isChange: false,
          })
        );
        this.viewChanges();
      });
    });
  }

  copyScore() {
    const copyText = [`**Замовлення № ${this.idOrder}**\n\n`];
    const sumAll = +this.sumAll(true).split('/')[0].trim();
    this.orderForm.value.forEach((order, i) => {
      const type = modelsData[order.article.substring(0, 3)] || modelsData[order.article.substring(0, 2)] || '';
      copyText.push(
        `${i + 1}. ${type}, колір ${order.colors}, код ${order.article}, кількість ${order.qty_pars} ${
          type.includes('брелок') ? 'шт' : 'пар'
        }, ціна ${formatNumber(order.price)} грн/${type.includes('брелок') ? 'шт' : 'пара'}\n`
      );
    });

    copyText.push(
      `Прогнозована дата виготовлення ${
        this.dataPlaneOrder ? [this.dataPlaneOrder.year, this.dataPlaneOrder.month, this.dataPlaneOrder.day].join('-') : null
      } \n\n`
    );
    copyText.push(`**Всього до оплати ${formatNumber(sumAll)}** грн\n`);
    copyText.push(`Аванс від ${formatNumber(Math.floor((sumAll * 0.3) / 100) * 100)} грн \n\n`);
    copyText.push(
      `**Обов'язково вказуйте призначення платежу: "Рахунок П-${this.idOrder}"**, а після оплати проінформуйте нас про транзакцію.\n\n`
    );
    copyText.push('**Якщо Вам потрібно рахунок і накладна у паперовому вигляді, попередьте нас і ми покладемо їх до замовлення.** \n');
    navigator.clipboard.writeText(copyText.join(''));
    this.isShowSpinner = false;
    this.alert = {
      isShow: true,
      type: 'success',
      message: 'Дані скопіювано',
    };
    setTimeout(() => {
      this.alertChange(false);
    }, 3000);
  }

  makeOrderDone() {
    this._serviceMain.changeFulfilled(this.idOrder, { status_order: !this.fulfilledOrder }).subscribe(() => {
      this.fulfilledOrder = !this.fulfilledOrder;
    });
  }

  alertChange(e) {
    this.alert.isShow = e;
  }

  changedate() {
    console.log(this.dataPlaneOrder);
  }
  isEmptyObject(obj) {
    if (obj === null) {
      return true;
    }
    return obj && Object.keys(obj).length === 0;
  }

  isDisabledBtn(mode: string) {
    const isClientsFormValid = this.isRecipient ? this.clientForm.valid && this.recipientForm.valid : this.clientForm.valid;
    const isOrderValid = this.orderForm.valid;
    // console.log(this.isNew ? (this.isNew && isClientsFormValid && isOrderValid) : true);
    // console.log(this.isNew, isClientsFormValid, isOrderValid, this.dataPlaneOrder, this.isEmptyObject(this.dataPlaneOrder));

    return mode === 'new'
      ? this.isNew
        ? !(this.isNew && isClientsFormValid && isOrderValid && !this.isEmptyObject(this.dataPlaneOrder))
        : true
      : !this.isNew
      ? !(!this.isNew && isClientsFormValid && isOrderValid && !this.isEmptyObject(this.dataPlaneOrder))
      : true;
  }
}
