import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { switchMap } from 'rxjs';
@Injectable({
  providedIn: 'root',
})
export class NovaPoshtaService {
  url = `https://api.novaposhta.ua/v2.0/json/`;
  apiKey: string = this._apiKeyNP;
  CounterpartyRef: string; // Recipient
  ContactRecipientRefSender: string; // Sender
  ContactRecipientRef: string;
  SenderAddress: string;
  RecipientAddress: string;
  ContactSender: string;
  ContactRecipient: string;
  constructor(private _http: HttpClient, @Inject('API_KEY_NP') private _apiKeyNP: string) {}

  getCities(city) {
    return this._http.post(`${this.url}`, {
      apiKey: this.apiKey,
      modelName: 'Address',
      calledMethod: 'searchSettlements',
      methodProperties: {
        CityName: city,
        Limit: 50,
      },
    });
  }

  getWarehouses(city) {
    return this._http.post(`${this.url}`, {
      modelName: 'Address',
      calledMethod: 'getWarehouses',
      methodProperties: {
        CityRef: city,
      },
      apiKey: this.apiKey,
    });
  }

  getCounterpartyRef(type: 'Sender' | 'Recipient' = 'Sender') {
    this._http
      .post(`${this.url}`, {
        apiKey: this.apiKey,
        modelName: 'Counterparty',
        calledMethod: 'getCounterparties',
        methodProperties: {
          CounterpartyProperty: type,
          Page: '1',
        },
      })
      .subscribe((data: any) => {
        if (type === 'Sender') {
          this.ContactRecipientRefSender = data.data[0].Ref;
        } else {
          this.CounterpartyRef = data.data[0].Ref;
        }
      });
  }

  getCounterpartyAddreses(type: 'Sender' | 'Recipient' = 'Sender') {
    this._http
      .post(`${this.url}`, {
        apiKey: this.apiKey,
        modelName: 'Counterparty',
        calledMethod: 'getCounterpartyAddresses',
        methodProperties: {
          Ref: this.ContactRecipientRefSender,
          CounterpartyProperty: type,
          Page: '1',
        },
      })
      .subscribe((data: any) => {
        if (type === 'Sender') {
          this.SenderAddress = data.data[0].Ref;
        } else {
          this.RecipientAddress = data.data[0].Ref;
        }
      });
  }

  createInternetDocument(params) {
    params = {
      ...params,
      Sender: this.ContactRecipientRefSender,
      Recipient: this.CounterpartyRef,
      ContactRecipient: this.ContactRecipient,
      ContactSender: this.ContactSender,
    };

    return this._http.post(`${this.url}`, {
      apiKey: this.apiKey,
      modelName: 'InternetDocument',
      calledMethod: 'save',
      methodProperties: params,
    });
  }

  getIdentifikator(params) {
    return this._http
      .post(`${this.url}`, {
        apiKey: this.apiKey,
        modelName: 'Counterparty',
        calledMethod: 'getCounterpartyAddresses',
        methodProperties: {
          Ref: this.ContactRecipientRefSender,
          CounterpartyProperty: 'Sender',
        },
      })
      .pipe(
        switchMap(() => {
          return this._http.post(`${this.url}`, {
            apiKey: this.apiKey,
            modelName: 'ContactPerson',
            calledMethod: 'save',
            methodProperties: {
              CounterpartyRef: this.CounterpartyRef,
              FirstName: params.first_name_client,
              LastName: params.second_name_client,
              Phone: params.phone,
            },
          });
        }),
        switchMap((data: any) => {
          this.ContactRecipient = data.data[0].Ref;
          return this._http.post(`${this.url}`, {
            apiKey: this.apiKey,
            modelName: 'ContactPersonGeneral',
            calledMethod: 'getContactPersonsList',
            methodProperties: {
              ContactProperty: 'Sender',
              CounterpartyRef: this.ContactRecipientRefSender,
              FindByString: '',
              Limit: 200,
              Page: 1,
            },
          });
        })
      )
      .subscribe((data: any) => {
        this.ContactSender = data.data[0].Ref;
      });
  }

  getPackList() {
    return this._http.post(`${this.url}`, {
      apiKey: this.apiKey,
      modelName: 'Common',
      calledMethod: 'getPackList',
      methodProperties: {},
    });
  }
}
