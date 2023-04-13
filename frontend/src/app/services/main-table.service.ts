import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class MainPageService {
    
    url = `${this._apiUrl}/main`;
    
    constructor(private _http: HttpClient, @Inject('API_URL') private _apiUrl: string) {}
    
    getListMain() { //залишати
        return this._http.get(this.url);
    }

    changeFulfilled(id, params) {
        return this._http.put(`${this.url}/status/${id}`, params);
    }

    sendPhase(id, params) { // delete
        return this._http.put(`${this.url}/phase/${id}`, params);
    }

    changePhase(id, params) {
        return this._http.put(`${this.url}/phase/${id}`, params)
    }

    sendFilters(params) {
        return this._http.get(this.url, {params});
    }
}
