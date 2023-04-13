import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class ClientService {
  url: string = `${this.apiUrl}/client`;

  constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

  saveClient(params) {
    return this.http.post(`${this.url}`, params);
  }

  getClient(id: string) {
    return this.http.get(`${this.url}/${id}`);
  }

  editClient(params, id) {
    return this.http.put(`${this.url}/${id}`, params);
  }
}
