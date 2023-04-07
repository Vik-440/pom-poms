import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class ClientService {
  url: string = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {}

  saveClient(params) {
    return this.http.post(`${this.url}/client`, params);
  }

  getClient(id: string) {
    return this.http.get(`${this.url}/client/${id}`);
  }

  editClient(params, id) {
    return this.http.put(`${this.url}/client/${id}`, params);
  }
}
