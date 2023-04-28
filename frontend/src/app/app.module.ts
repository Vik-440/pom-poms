import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgSelectModule } from '@ng-select/ng-select';
// import { TooltipModule, TooltipOptions } from '@teamhive/ngx-tooltip';
import { ClickOutsideModule } from 'ng-click-outside';
import { DatepickerModule } from 'ng2-datepicker';
import { NgxMaskModule } from 'ngx-mask';
import { NgxSpinnerModule } from 'ngx-spinner';
import { environment } from 'src/environments/environment';
import { AlertComponent } from './alert/alert.component';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CreateOrderComponent } from './create-order/create-order.component';
import { FinancesComponent } from './finances/finances.component';
import { NavbarComponent } from './navbar/navbar.component';
import { ReserveComponent } from './reserve/reserve.component';
import { MainTableComponent } from './main-table/main-table.component';
import { ClientFormComponent } from './client-form/client-form.component';
@NgModule({
    declarations: [
        AppComponent,
        NavbarComponent,
        CreateOrderComponent,
        ReserveComponent,
        FinancesComponent,
        AlertComponent,
        MainTableComponent,
        ClientFormComponent,
    ],
    imports: [
        BrowserAnimationsModule,
        NgxMaskModule.forRoot(),
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        ClickOutsideModule,
        NgbModule,
        CommonModule,
        DatepickerModule,
        FormsModule,
        NgSelectModule,
        NgxSpinnerModule,
        ReactiveFormsModule,
    ],
    providers: [{ provide: 'API_URL', useValue: environment.apiUrl }],
    bootstrap: [AppComponent],
    schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class AppModule {}
