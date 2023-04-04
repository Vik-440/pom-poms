import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class ClientService { 
  url: string = 'http://127.0.0.1:5000';
  
  constructor(private http: HttpClient,) {}

  getClient(id: string) {
    return this.http.get(`${this.url}/read_client/${id}`)
  }
}