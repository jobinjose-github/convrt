import { NgClass } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterModule } from '@angular/router';

interface RefsTable {
  title: string,
  path: string
}

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, RouterModule, NgClass],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  refsTable: RefsTable[] = [
    {
      "title": "Features",
      "path": "/features"
    },
    {
      "title": "Pricing",
      "path": "/pricing"
    },
    {
      "title": "API",
      "path": "/api"
    },
    {
      "title": "Signup",
      "path": "/signup"
    },
    {
      "title": "Login",
      "path": "/login"
    },
  ];
  isHamburgerActive: boolean = false;

  toggleHamburger(){
    this.isHamburgerActive = !this.isHamburgerActive
  }
}
