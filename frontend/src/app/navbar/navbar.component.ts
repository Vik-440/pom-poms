import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.sass']
})
export class NavbarComponent implements OnInit {
  [x: string]: any;

  constructor(private router: Router) { }

  navbarCollapsed = true;
  ngOnInit(): void {

  }

  reloadCurrentRoute() {
    window.location.reload();
  }
}
