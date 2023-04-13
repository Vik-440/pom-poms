import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
    providedIn: 'root',
})
export class MaterialPageService {
    url = `${this._apiUrl}/material`;

    constructor(private _http: HttpClient, @Inject('API_URL') private _apiUrl: string) {}

    getListMaterial() {
        return this._http.get(this.url);
    }

    getFullInfoMaterial(id) {
        const params = {
            id_color: id,
        };
        return this._http.post(this.url, params);
    }

    getFullAllMaterial(params) {
        return this._http.post(this.url, params);
    }

    saveMaterial(data) {
        return this._http.post(this.url, data);
    }
}
