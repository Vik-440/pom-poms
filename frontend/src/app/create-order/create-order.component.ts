import { Component, Input, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import locale from 'date-fns/locale/en-US';
import * as moment from 'moment';
import { DatepickerOptions } from 'ng2-datepicker';
import { NgxSpinnerService } from 'ngx-spinner';
import { filter, tap } from 'rxjs';
import { modelsData } from 'src/assets/models-data/modelsData';
import { formatNumber } from 'src/common/common';
import { CreateOrderService } from '../services/create-order.service';
import { MainPageService } from '../services/main-table.service';
@Component({
    selector: 'app-create-order',
    templateUrl: './create-order.component.html',
    styleUrls: ['./create-order.component.sass'],
})
export class CreateOrderComponent implements OnInit {
    constructor(
        private fb: FormBuilder,
        private service: CreateOrderService,
        private spinner: NgxSpinnerService,
        private route: ActivatedRoute,
        private serviceMain: MainPageService
    ) {}

    @Input() isNew: Boolean = true;
    displayMonths = 2;
    isShowSpinner = false;
    model: NgbDateStruct;
    navigation = 'select';
    showWeekNumbers = false;
    outsideDays = 'visible';

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

    orders = [1];

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
    commentOrder = '';
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
        this.dataPlaneOrder = JSON.parse(localStorage.getItem('data_plane_order')) || null;
        this.dateToday = JSON.parse(localStorage.getItem('dateToday')) || null;
        if (this.route.snapshot.params.id) {
            this.idOrder = +this.route.snapshot.params.id;
            this.getOrder();
        } else if (this.route.snapshot.params.codeModel) {
            this.chooseKode(this.route.snapshot.params.codeModel, 0, false);
        } else if (this.route.snapshot.params.phoneClient) {
            this.selectedItemClient(
                this.route.snapshot.params.phoneClient,
                'sl_phone',
                this.clientForm,
                'isSaveClient',
                false
            );
        } else if (this.route.snapshot.params.phoneRecipient) {
            this.isRecipient = true;
            this.selectedItemClient(
                this.route.snapshot.params.phoneRecipient,
                'sl_phone',
                this.recipientForm,
                'isSaveRecipient',
                false
            );
        }
    }

    requiredFalse(){
        return (control) => {
            return control.value
          }
    }

    init() {
        this.commentOrder = '';
        this.isSaveClient = false;
        this.isSaveRecipient = false;
        this.dateForms = this.fb.group({
            data_order: moment().format('YYYY-MM-DD'),
            data_plane_order: null,
            data_send_order: null,
        });

        this.priceAll = this.fb.group({
            sum_payment: 0,
            real_money: 0,
            different: 0,
        });

        this.orderForm = this.fb.array([
            this.fb.group({
                kod_model: null,
                id_model: null,
                kolor_model: null,
                id_color_1: null,
                name_color_1: null,
                id_color_part_1: null,
                id_color_2: null,
                name_color_2: null,
                id_color_part_2: null,
                id_color_3: null,
                name_color_3: null,
                id_color_part_3: null,
                id_color_4: null,
                name_color_4: null,
                id_color_part_4: null,
                price_model: null,
                quantity_pars_model: [null, Validators.required],
                phase_1: 0,
                phase_2: 0,
                phase_3: 0,
                phase_1_default: 0,
                phase_2_default: 0,
                phase_3_default: 0,
                sum_pars: null,
                comment_model: null,
                isNew: [true, this.requiredFalse()],
                isChange: false,
            }),
        ]);

        this.clientForm = this.fb.group({
            id_client: null,
            phone_client: [null, Validators.required],
            second_name_client: [null, Validators.required],
            first_name_client: [null, Validators.required],
            surname_client: null,
            sity: [null, Validators.required],
            np_number: [null, Validators.required],
            name_team: null,
            coach: null,
            zip_code: null,
            street_house_apartment: null,
            comment_client: null,
        });

        this.recipientForm = this.fb.group({
            id_client: null,
            coach: null,
            phone_client: [null, Validators.required],
            second_name_client: [null, Validators.required],
            first_name_client: [null, Validators.required],
            surname_client: null,
            sity: [null, Validators.required],
            np_number: [null, Validators.required],
            name_team: null,
            zip_code: null,
            street_house_apartment: null,
            comment_client: null,
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
            sumAllItems.push(
                this.priceAll.value.sum_payment - this.discount,
                this.priceAll.value.real_money,
                this.priceAll.value.different
            );
        } else {
            sumAllItems.push(
                this.priceAll.value.sum_payment,
                this.priceAll.value.real_money,
                this.priceAll.value.different
            );
        }
        return sumAllItems.join(' / ');
    }

    viewChanges() {
        this.orderForm.controls.map((order, index) => {
            order
                .get('quantity_pars_model')
                .valueChanges.pipe(
                    tap((data) => {
                        const type =
                            modelsData[order.value.kod_model?.substring(0, 3)] ||
                            modelsData[order.value.kod_model?.substring(0, 2)] ||
                            '';

                        order.patchValue({
                            sum_pars: data * order.value.price_model,
                            phase_1: order.value.phase_1_default + (type.includes('брелок') ? +data : +(data * 2)),
                            phase_2: order.value.phase_2_default + (type.includes('брелок') ? +data : +(data * 2)),
                            phase_3: order.value.phase_3_default + +data,
                        });
                    })
                )
                .subscribe();

            order
                .get('price_model')
                .valueChanges.pipe(
                    tap((data) => {
                        order.patchValue({
                            sum_pars: data * order.value.quantity_pars_model,
                            isNew: true,
                        });
                    })
                )
                .subscribe();

            order.get('id_color_1').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });

            order.get('id_color_2').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });

            order.get('id_color_3').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });

            order.get('id_color_4').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });

            order.get('kod_model').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });

            order.get('kolor_model').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });

            order.get('id_color_part_1').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });

            order.get('id_color_part_2').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });

            order.get('id_color_part_3').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });

            order.get('id_color_part_4').valueChanges.subscribe(() => {
                order.patchValue({
                    isNew: true,
                });
            });
        });

        this.recipientForm.valueChanges.subscribe(() => {
            if (this.isSaveRecipient) {
                this.isSaveRecipient = false;
            }
        });

        this.clientForm.valueChanges.subscribe(() => {
            if (this.isSaveClient) {
                this.isSaveClient = false;
            }
        });
    }

    changeKodModel(value) {
        if (value.length >= 3) {
            this.service.getInfoForOrder({ ur_kod: value }).subscribe((kods: any) => {
                this.kodItems = kods?.kod_model;
            });
        }
    }

    changeMaterial(value, index) {
        if (value.length >= 3) {
            this.service.getInfoForOrder({ ur_kolor: value }).subscribe((materials: any) => {
                this.materialsItems = materials;
            });
        }
    }

    chooseKode(value, index, ignore = true) {
        if (!this.kodItems) {
            this.orderForm.controls.map((order, ind) => {
                if (ind === index && value) {
                    order.patchValue({
                        kod_model: value,
                    });
                } else if (!value) {
                    order.patchValue({
                        kod_model: null,
                    });
                }
                return;
            });
        }
        if (this.kodItems?.includes(value) || !ignore) {
            this.orderForm.controls.map((order, ind) => {
                this.service.getInfoForOrder({ sl_kod: value }).subscribe((data: any) => {
                    if (index === ind && Object.keys(data).length) {
                        order.patchValue(
                            {
                                id_model: data.id_model,
                                kod_model: data.kod_model,
                                kolor_model: data.kolor_model,
                                name_color_1: data.name_color_1 || null,
                                id_color_part_1: data.id_color_part_1,
                                id_color_1: data.id_color_1,
                                id_color_2: data.id_color_2,
                                id_color_3: data.id_color_3,
                                id_color_4: data.id_color_4,
                                name_color_2: data.name_color_2 || null,
                                id_color_part_2: data.id_color_part_2,
                                name_color_3: data.name_color_3 || null,
                                id_color_part_3: data.id_color_part_3,
                                name_color_4: data.name_color_4 || null,
                                id_color_part_4: data.id_color_part_4,
                                price_model: data.price_model,
                                comment_model: data.comment_model,
                                isNew: false,
                                isChange: false,
                            },
                            { emitEvent: false }
                        );
                    }
                });
            });
        }
        this.kodItems = [];
    }

    changeIdColor(order, field, value) {
        order.patchValue({
            [field]: value.id_color,
        });
        this.resetMaterialsItems();
    }

    resetMaterialsItems() {
        this.materialsItems = [];
    }

    changeCoach(form, field) {
        if (form.value[field] === form.value.second_name_client) {
            form.patchValue({
                [field]: null,
            });
        } else {
            form.patchValue({
                [field]: form.value.second_name_client,
            });
        }
    }

    addOrder() {
        this.orderForm.push(
            this.fb.group({
                kod_model: null,
                id_model: null,
                kolor_model: null,
                id_color_1: null,
                name_color_1: null,
                name_color_2: null,
                name_color_3: null,
                name_color_4: null,
                id_color_part_1: null,
                id_color_2: null,
                id_color_part_2: null,
                id_color_3: null,
                id_color_part_3: null,
                id_color_4: null,
                id_color_part_4: null,
                price_model: null,
                quantity_pars_model: [null, Validators.required],
                phase_1: 0,
                phase_2: 0,
                phase_3: 0,
                phase_1_default: 0,
                phase_2_default: 0,
                phase_3_default: 0,
                sum_pars: null,
                comment_model: null,
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

    saveOrder(index, order) {
        const params = {
            sl_id_model: order.value.id_model || 0,
            kod_model: order.value.kod_model || 0,
            id_color_1: order.value.id_color_1 || 0,
            id_color_part_1: +order.value.id_color_part_1 || 0,
            id_color_2: +order.value.id_color_2 || 0,
            id_color_part_2: +order.value.id_color_part_2 || 0,
            id_color_3: +order.value.id_color_3 || 0,
            id_color_part_3: +order.value.id_color_part_3 || 0,
            id_color_4: +order.value.id_color_4 || 0,
            id_color_part_4: +order.value.id_color_part_4 || 0,
            price_model: order.value.price_model || 0,
            comment_model: order.value.comment_model,
            kolor_model: order.value.kolor_model || 0,
        };
        this.isShowSpinner = true;
        this.service.getInfoForOrder(params).subscribe(
            (data: any) => {
                order.patchValue({
                    isNew: false,
                    id_model: data.id_model,
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

    changeClientInfo(query, minLength, keySend) {
        if (query.length >= minLength) {
            this.service.getInfoForOrder({ [keySend]: query }).subscribe((data: any) => {
                if (keySend === 'ur_second_name') {
                    this.clientDataItems = [];
                    data.id_client.forEach((item, i) => {
                        this.clientDataItems.push({
                            id: item,
                            secondName: data.second_name_client[i],
                        });
                    });
                } else {
                    this.clientDataItems = [...new Set([...Object.values(data)].flat())];
                }
            });
        }
    }

    selectedItemClient(value, keySend, form = this.clientForm, saveBtn = 'isSaveClient', ignore = true) {
        if (value && keySend === 'open_id_client' && this.clientDataItems.includes(value)) {
            value = value.id;
            this.sendDataClient(value, keySend, form, saveBtn);
        }
        if ((value && this.clientDataItems.includes(value)) || !ignore) {
            this.sendDataClient(value, keySend, form, saveBtn);
        }

        form.patchValue({
            second_name_client: value.secondName || value
        });
        this.clientDataItems = [];
    }

    sendDataClient(value, keySend, form, saveBtn) {
        this.service
            .getInfoForOrder({ [keySend]: value })
            .pipe(filter(() => value))
            .subscribe((dataClient: any) => {
                form.setValue(
                    {
                        coach: dataClient?.coach,
                        comment_client: dataClient.comment_client,
                        first_name_client: dataClient.first_name_client,
                        id_client: dataClient.id_client,
                        name_team: dataClient.name_team,
                        phone_client: dataClient.phone_client,
                        second_name_client: dataClient.second_name_client,
                        sity: dataClient.sity,
                        street_house_apartment: dataClient.street_house_apartment,
                        surname_client: dataClient.surname_client,
                        zip_code: dataClient.zip_code,
                        np_number: dataClient.np_number,
                    },
                    { emitEvent: false }
                );
                this[saveBtn] = true;
            });
    }
    clearDataClient() {
        this.clientDataItems = [];
    }

    saveClient() {
        const params = {
            sl_id_recipient: null,
            phone_client: this.clientForm.value.phone_client,
            second_name_client: this.clientForm.value.second_name_client,
            first_name_client: this.clientForm.value.first_name_client,
            surname_client: this.clientForm.value.surname_client,
            np_number: this.clientForm.value.np_number,
            name_team: this.clientForm.value.name_team,
            coach: this.clientForm.value.coach,
            zip_code: this.clientForm.value.zip_code,
            street_house_apartment: this.clientForm.value.street_house_apartment,
            comment_client: this.clientForm.value.comment_client,
            sity: this.clientForm.value.sity,
        };
        this.isShowSpinner = true;
        this.service.getInfoForOrder(params).subscribe(
            (data: any) => {
                this.isShowSpinner = false;
                this.clientForm.patchValue({
                    id_client: data.id_recipient || this.clientForm.value.id_client,
                });
                this.isSaveClient = true;
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

    saveRecipient() {
        const params = {
            sl_id_recipient: null,
            phone_client: this.recipientForm.value.phone_client,
            second_name_client: this.recipientForm.value.second_name_client,
            first_name_client: this.recipientForm.value.first_name_client,
            surname_client: this.recipientForm.value.surname_client,
            np_number: this.recipientForm.value.np_number,
            id_team: this.recipientForm.value.id_team,
            coach: this.clientForm.value.coach,
            name_team: this.clientForm.value.name_team,
            zip_code: this.recipientForm.value.zip_code,
            street_house_apartment: this.recipientForm.value.street_house_apartment,
            comment_client: this.recipientForm.value.comment_client,
            sity: this.recipientForm.value.sity,
        };
        this.isShowSpinner = true;
        this.service.getInfoForOrder(params).subscribe(
            (data: any) => {
                this.recipientForm.patchValue({
                    id_client: data.id_recipient,
                });
                // this.isSaveClient = true;
                this.isShowSpinner = false;
                this.isSaveRecipient = true;
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

    makeArrayDataOrder(key, i = 0) {
        const result = [];
        if (this.orderForm.value[0][key] !== undefined) {
            this.orderForm.value.map((order) => {
                result.push(+order[key] || 0);
            });
        }
        return result;
    }

    saveAll(mode = 'create') {
        const params = {
            id_order: +this.idOrder,
            data_order: [this.dateToday.year, this.dateToday.month, this.dateToday.day].join('-'),
            id_client: this.clientForm.value.id_client,
            id_recipient: !this.isRecipient ? this.clientForm.value.id_client : this.recipientForm.value.id_client, // (2 або ід_клієнт)
            id_model: this.makeArrayDataOrder('id_model'),
            price_model_order: this.makeArrayDataOrder('price_model'),
            quantity_pars_model: this.makeArrayDataOrder('quantity_pars_model'),
            phase_1: this.makeArrayDataOrder('phase_1'),
            phase_2: this.makeArrayDataOrder('phase_2'),
            phase_3: this.makeArrayDataOrder('phase_3'),
            data_plane_order: this.dataPlaneOrder
                ? [this.dataPlaneOrder.year, this.dataPlaneOrder.month, this.dataPlaneOrder.day].join('-')
                : null, // - прогнозована
            discont_order: this.discount,
            sum_payment: +this.sumAll(false).split('/')[0].trim(),
            fulfilled_order: false,
            comment_order: this.commentOrder,
            edit_real_order: this.idOrder,
        };

        if (mode === 'create') {
            delete params.edit_real_order;
        }

        this.service.saveOrder(params).subscribe((data: any) => {
            this.idOrder = +data.id_order || this.idOrder;
            this.doneOrder = true;
            localStorage.setItem('data_plane_order', JSON.stringify(this.dataPlaneOrder));
            localStorage.setItem('dateToday', JSON.stringify(this.dateToday));
        });
    }

    setClientData(dataClient) {
        this.clientForm.setValue(
            {
                coach: dataClient?.coach,
                comment_client: dataClient.comment_client,
                first_name_client: dataClient.first_name_client,
                id_client: dataClient.id_client,
                name_team: dataClient.name_team,
                phone_client: dataClient.phone_client,
                second_name_client: dataClient.second_name_client,
                sity: dataClient.sity,
                street_house_apartment: dataClient.street_house_apartment,
                surname_client: dataClient.surname_client,
                zip_code: dataClient.zip_code,
                np_number: dataClient.np_number,
            },
            { emitEvent: false }
        );
        this.isSaveClient = true;
        this.viewChanges();
    }

    setRecipientData(dataRecipient) {
        this.recipientForm.setValue(
            {
                coach: dataRecipient?.coach,
                comment_client: dataRecipient.comment_client,
                first_name_client: dataRecipient.first_name_client,
                id_client: dataRecipient.id_client,
                name_team: dataRecipient.name_team,
                phone_client: dataRecipient.phone_client,
                second_name_client: dataRecipient.second_name_client,
                sity: dataRecipient.sity,
                street_house_apartment: dataRecipient.street_house_apartment,
                surname_client: dataRecipient.surname_client,
                zip_code: dataRecipient.zip_code,
                np_number: dataRecipient.np_number,
            },
            { emitEvent: false }
        );

        this.isSaveRecipient = true;
        this.viewChanges();
    }

    getOrder() {
        const params = {
            edit_order: this.idOrder,
        };
        this.isShowSpinner = true;
        this.service
            .getInfoForOrder(params)
            .pipe(
                tap(() => {
                    this.isShowSpinner = true;
                })
            )
            .subscribe((data: any) => {
                if (Object.keys(data).length) {
                    const arrDataOrder = data.data_order.split('-');
                    const arrDataPlane = data.data_plane_order.split('-');
                    this.commentOrder = data.comment_order;
                    this.dateToday = { year: +arrDataOrder[0], month: +arrDataOrder[1], day: +arrDataOrder[2] };
                    this.dataPlaneOrder = { year: +arrDataPlane[0], month: +arrDataPlane[1], day: +arrDataPlane[2] };
                    this.discount = data.discont_order;
                    this.fulfilledOrder = data.fulfilled_order;
                    this.service.getInfoForOrder({ open_id_client: data.id_client }).subscribe((dataClient: any) => {
                        this.isShowSpinner = false;
                        this.setClientData(dataClient);
                        if (data.id_client !== data.id_recipient) {
                            this.isRecipient = true;
                            this.service
                                .getInfoForOrder({ open_id_client: data.id_recipient })
                                .subscribe((dataRecipient: any) => {
                                    this.setRecipientData(dataRecipient);
                                    this.getModels(data);
                                });
                        } else {
                            this.getModels(data);
                        }
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
                }
            });
    }
    getModels(data) {
        data.id_model.forEach((model, index) => {
            if (index === 0) {
                this.orderForm.clear();
            }

            this.service.getInfoForOrder({ open_id_model: model }).subscribe((dataModel: any) => {
                this.orderForm.push(
                    this.fb.group({
                        id_model: dataModel.id_model,
                        kod_model: dataModel.kod_model,
                        kolor_model: dataModel.kolor_model,
                        name_color_1: dataModel.name_color_1 || null,
                        id_color_part_1: dataModel.id_color_part_1,
                        id_color_1: dataModel.id_color_1,
                        id_color_2: dataModel.id_color_2,
                        id_color_3: dataModel.id_color_3,
                        id_color_4: dataModel.id_color_4,
                        name_color_2: dataModel.name_color_2 || null,
                        id_color_part_2: dataModel.id_color_part_2,
                        name_color_3: dataModel.name_color_3 || null,
                        id_color_part_3: dataModel.id_color_part_3,
                        name_color_4: dataModel.name_color_4 || null,
                        id_color_part_4: dataModel.id_color_part_4,
                        price_model: data.price_model_order[index],
                        phase_1: data.phase_1[index],
                        phase_2: data.phase_2[index],
                        phase_3: data.phase_3[index],
                        phase_1_default: data.phase_1[index],
                        phase_2_default: data.phase_2[index],
                        phase_3_default: data.phase_3[index],
                        comment_model: dataModel.comment_model,
                        quantity_pars_model: [data.quantity_pars_model[index], Validators.required],
                        sum_pars: data.quantity_pars_model[index] * data.price_model_order[index],
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
            const type =
                modelsData[order.kod_model.substring(0, 3)] || modelsData[order.kod_model.substring(0, 2)] || '';
            copyText.push(
                `${i + 1}. ${type}, колір ${order.kolor_model}, код ${order.kod_model}, кількість ${
                    order.quantity_pars_model
                } ${type.includes('брелок') ? 'шт' : 'пар'}, ціна ${formatNumber(order.price_model)} грн/${
                    type.includes('брелок') ? 'шт' : 'пара'
                }\n`
            );
        });

        copyText.push(
            `Прогнозована дата виготовлення ${
                this.dataPlaneOrder
                    ? [this.dataPlaneOrder.year, this.dataPlaneOrder.month, this.dataPlaneOrder.day].join('-')
                    : null
            } \n\n`
        );
        copyText.push(`**Всього до оплати ${formatNumber(sumAll)}** грн\n`);
        copyText.push(`Аванс від ${formatNumber(Math.floor((sumAll * 0.3) / 100) * 100)} грн \n\n`);
        copyText.push(
            `**Обов'язково вказуйте призначення платежу: "Рахунок П-${this.idOrder}"**, а після оплати проінформуйте нас про транзакцію.\n\n`
        );
        copyText.push(
            `**Якщо Вам потрібно рахунок і накладна у паперовому вигляді, попередьте нас і ми покладемо їх до замовлення.** \n`
        );
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
        this.serviceMain
            .makeDoneOrder({
                fulfilled_id_order: this.idOrder,
                fulfilled_order: !this.fulfilledOrder,
            })
            .subscribe(() => {
                this.fulfilledOrder = !this.fulfilledOrder;
            });
    }

    alertChange(e) {
        this.alert.isShow = e;
    }
}
