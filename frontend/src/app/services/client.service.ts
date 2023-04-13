import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class ClientService {
  url: string = `${this._apiUrl}/client`;

  constructor(private _http: HttpClient, @Inject('API_URL') private _apiUrl: string) {}

  saveClient(params) {
    return this._http.post(`${this.url}`, params);
  }

  getClient(id: string) {
    return this._http.get(`${this.url}/${id}`);
  }

  editClient(params, id) {
    return this._http.put(`${this.url}/${id}`, params);
  }
}
