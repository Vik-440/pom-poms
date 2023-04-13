import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
    providedIn: 'root',
})
export class MaterialPageService {
    url = `${this.apiUrl}/material`;

    constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

    getListMaterial() {
        return this.http.get(this.url);
    }

    getFullInfoMaterial(id) {
        const params = {
            id_color: id,
        };
        return this.http.post(this.url, params);
    }

    getFullAllMaterial(params) {
        return this.http.post(this.url, params);
    }

    saveMaterial(data) {
        return this.http.post(this.url, data);
    }
}
