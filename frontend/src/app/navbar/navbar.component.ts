import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

@Component({
    selector: 'app-navbar',
    templateUrl: './navbar.component.html',
    styleUrls: ['./navbar.component.sass'],
})
export class NavbarComponent {
    [x: string]: any;

    constructor(private _router: Router, public _location: Location) {
        this._router.routeReuseStrategy.shouldReuseRoute = () => false;
    }

    navbarCollapsed = true;
}
