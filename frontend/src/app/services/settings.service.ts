import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class SettingsService {
  url = `${this._apiUrl}`;

  constructor(private _http: HttpClient, @Inject('API_URL') private _apiUrl: string) {}

  getAppSettings() {
    return this._http.get(`${this.url}/param`);
  }

  createAppSetting(params) {
    return this._http.post(`${this.url}/param`, params);
  }

  updateAppSetting(setting, params) {
    params = {
      ...params,
      parameter_str: JSON.stringify(params.parameter_str),
    }
    return this._http.put(`${this.url}/param/${setting}`, params);
  }
  getInfoAboutAppSetting(params) {
    return this._http.get(`${this.url}/param/${params}`);
  }
}
