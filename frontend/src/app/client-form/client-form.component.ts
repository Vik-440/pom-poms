import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { filter } from 'rxjs';
import { ClientService } from '../services/client.service';
import { CreateOrderService } from '../services/create-order.service';
import { DataAutofill } from './autofill';

@Component({
  selector: 'app-client-form',
  templateUrl: './client-form.component.html',
  styleUrls: ['./client-form.component.sass'],
})
export class ClientFormComponent implements OnInit {
  @Input() clientForm: FormGroup;
  @Input() isClient: boolean = true;
  @Input() isShowOk: boolean = false;
  @Output() saveFormEmitter: EventEmitter<any> = new EventEmitter();

  clientDataItems;
  isNewForm: boolean = true;
  callAfterViewChecked = true;

  constructor(private service: CreateOrderService, private clientService: ClientService) {}

  ngOnInit() {
    this.clientForm.valueChanges.subscribe(() => {
      if(this.isShowOk) {
        this.isNewForm = false;
      }
      this.isShowOk = false;
    })
  }

  changeClientInfo(query, keySend) {
    if (query.length >= DataAutofill[keySend]) {
      this.service.getAutofill({ [keySend]: query }).subscribe((data: any) => {
        this.clientDataItems = [...data];
      });
    }
  }

  selectItem(value) {
    if(value && value.hasOwnProperty('id_client')) {
      this.clientService.getClient(value.id_client).subscribe((data) => {
        this.isNewForm = false;
        this.setValueForm(data);
      });
    }
    this.clearDataClient();
  }

  setValueForm(dataClient) {
    this.clientForm.patchValue(
      {
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

    if(this.isClient) {
      this.clientForm.patchValue({
        coach: dataClient?.coach,
      }, { emitEvent: false })
    }
  }
  clearDataClient() {
    this.clientDataItems = [];
  }

  saveForm(isNew) {
    this.saveFormEmitter.emit({
      isClient: this.isClient,
      isNew
    })
  }
 }
