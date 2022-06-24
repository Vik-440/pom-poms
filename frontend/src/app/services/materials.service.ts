import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class MaterialPageService {

  url = `${this.apiUrl}/main_page`;

  constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {
  }

  getListMaterial() {
    return this.http.get(`http://127.0.0.1:5000/material`);
  }

  getFullInfoMaterial(id) {
    const params = {
      id_color: id
    };
    return this.http.post(`http://127.0.0.1:5000/material`, params);
  }

  getFullAllMaterial(params) {
    return this.http.post(`http://127.0.0.1:5000/material`, params);
  }

  saveMaterial(data) {
    console.log(data);
    
    return this.http.post(`http://127.0.0.1:5000/material`, data);
  }

}
