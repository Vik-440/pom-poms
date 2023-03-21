import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class MainPageService {
    url = `${this.apiUrl}/main`;

    constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}

    getListMain() { //залишати
        return this.http.get(`http://127.0.0.1:5000/main`);
    }


    makeDoneOrder(params) {
        return this.http.post(`http://127.0.0.1:5000/main_page`, params);
    }

    changeFulfilled(id, params) {
        return this.http.put(`http://127.0.0.1:5000/main/status/${id}`, params);
    }

    sendPhase(id, params) { // delete
        return this.http.put(`http://127.0.0.1:5000/main/phase/${id}`, params);
    }

    changePhase(id, params) {
        return this.http.put(`http://127.0.0.1:5000/main/phase/${id}`, params)
    }

    sendFilters(params) {
        return this.http.get(`http://127.0.0.1:5000/main`, {params});
    }
}
