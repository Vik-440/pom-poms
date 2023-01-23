import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateOrderComponent } from './create-order/create-order.component';
import { FinancesComponent } from './finances/finances.component';
import { MainTableComponent } from './main-table/main-table.component';
import { ReserveComponent } from './reserve/reserve.component';

const routes: Routes = [
    { path: '', component: MainTableComponent },
    { path: 'create-order', component: CreateOrderComponent },
    { path: 'materials', component: ReserveComponent },
    { path: 'finances-page', component: FinancesComponent },
];

@NgModule({
    imports: [RouterModule.forRoot(routes, { onSameUrlNavigation: 'reload' })],
    exports: [RouterModule],
})
export class AppRoutingModule {}
