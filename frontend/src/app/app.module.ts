import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgSelectModule } from '@ng-select/ng-select';
import { TooltipModule, TooltipOptions } from '@teamhive/ngx-tooltip';
import { DatepickerModule } from 'ng2-datepicker';
import { NgxMaskModule } from 'ngx-mask';
import { NgToggleModule } from 'ngx-toggle-button';
import { environment } from 'src/environments/environment';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CreateOrderComponent } from './create-order/create-order.component';
import { FinancesComponent } from './finances/finances.component';
import { NavbarComponent } from './navbar/navbar.component';
import { ReserveComponent } from './reserve/reserve.component';
import { SortDirective, TableComponent } from './table/table.component';
import { NgxSpinnerModule } from 'ngx-spinner';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
@NgModule({
    declarations: [
        AppComponent,
        SortDirective,
        TableComponent,
        NavbarComponent,
        CreateOrderComponent,
        ReserveComponent,
        FinancesComponent,
    ],
    imports: [
        NgToggleModule,
        BrowserAnimationsModule,
        NgxMaskModule.forRoot(),
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        NgbModule,
        CommonModule,
        DatepickerModule,
        FormsModule,
        NgSelectModule,
        NgxSpinnerModule,
        ReactiveFormsModule,
        TooltipModule.forRoot({
            placement: 'top',
            arrow: 'true',
            arrowType: 'sharp',
            allowHTML: true,
            maxWidth: 200,
        } as unknown as TooltipOptions),
    ],
    providers: [{ provide: 'API_URL', useValue: environment.apiUrl }],
    bootstrap: [AppComponent],
    schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class AppModule {}
