import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class UsefulService {
  url = `${this._apiUrl}`;

  constructor(private _http: HttpClient, @Inject('API_URL') private _apiUrl: string) {}

  getAutofill(params) {
    return this._http.get(`${this.url}/autofill`, { params });
  }
}
