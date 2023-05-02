import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
    providedIn: 'root',
})
export class MaterialPageService {
    url = `${this._apiUrl}/materials`;

    constructor(private _http: HttpClient, @Inject('API_URL') private _apiUrl: string) {}

    getListMaterial(params?) {
        return this._http.get(this.url, { params });
    }

    getFullInfoMaterial(id) {
        return this._http.get(`${this.url}/${id}`);
    }

    saveMaterial(data) {
        return this._http.post(this.url, data);
    }

    saveConsumptionMaterial(params, id) {
        return this._http.put(`${this.url}/consumption/${id}`, params);
    }

    editMaterial(data, id) {
        return this._http.put(`${this.url}/${id}`, data);
    }
}
