import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root',
})
export class MainPageService {
    
    url = `${this.apiUrl}/main`;
    
    constructor(private http: HttpClient, @Inject('API_URL') private apiUrl: string) {}
    
    getListMain() { //залишати
        return this.http.get(this.url);
    }

    changeFulfilled(id, params) {
        return this.http.put(`${this.url}/status/${id}`, params);
    }

    sendPhase(id, params) { // delete
        return this.http.put(`${this.url}/phase/${id}`, params);
    }

    changePhase(id, params) {
        return this.http.put(`${this.url}/phase/${id}`, params)
    }

    sendFilters(params) {
        return this.http.get(this.url, {params});
    }
}
