import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class FinancesPageService {
    url = `${this._apiUrl}/finance`;

    constructor(private _http: HttpClient, @Inject('API_URL') private _apiUrl: string) {}

    getFinances() {
        return this._http.get(this.url);
    }

    getMethods() {
        return this._http.get(`${this.url}/methods`);
    }

    getStaticPayments(params) {
        return this._http.post(`${this.url}/payments/statics`, params);
    }

    getFilters(params, urlEnd = '') {
        return this._http.post(`${this.url}${urlEnd}`, params);
    }

    getPayments() {
        return this._http.get(`${this.url}/payments`);
    }

    getOutlays() {
        return this._http.get(`${this.url}/outlays`);
    }

    editPayment(params) {
        return this._http.put(`${this.url}/payment/${params.id_payment}`, params);
    }

    savePayment(params) {
        return this._http.post(`${this.url}/payment`, params);
    }

    editOutlay(params) {
        return this._http.put(`${this.url}/outlay/${params.id_outlay}`, params);
    }

    saveOutlay(params) {
        return this._http.post(`${this.url}/outlay`, params);
    }

    getStatistics() {
        return this._http.post(this.url, { stat: 'all' });
    }
}
