import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { UntypedFormGroup } from '@angular/forms';
import { DataAutofillInterface } from '../interfaces/autofill-data';
import { ClientService } from '../services/client.service';
import { UsefulService } from '../services/useful.service';
import { DataAutofill } from '../utils/autofill';

@Component({
  selector: 'app-client-form',
  templateUrl: './client-form.component.html',
  styleUrls: ['./client-form.component.sass'],
})
export class ClientFormComponent implements OnInit {
  @Input() clientForm: UntypedFormGroup;
  @Input() isClient: boolean = true;
  @Input() isShowOk: boolean;
  @Output() saveFormEmitter: EventEmitter<any> = new EventEmitter();

  clientDataItems: DataAutofillInterface[];
  isNewForm: boolean = true;
  callAfterViewChecked: boolean = true;

  constructor(private _clientService: ClientService, private _usefulService: UsefulService) {}

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
      this._usefulService.getAutofill({ [keySend]: query }).subscribe((data: DataAutofillInterface[]) => {
        this.clientDataItems = [...data];
      });
    }
  }

  selectItem(value, field: string) {
    if(value && value.hasOwnProperty('id_client')) {
      this._clientService.getClient(value.id_client).subscribe((data) => {
        this.isNewForm = false;
        this.isShowOk = true;
        this.setValueForm(data);
      });
    } else if(value) {
      this.clientForm.patchValue({
        [field]: value.value,
      })
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
      isNew,
    })
  }
 }
