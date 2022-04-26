import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SortDirective } from './table.component';

describe('SortDirective', () => {
  let component: SortDirective;
  let fixture: ComponentFixture<SortDirective>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SortDirective ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SortDirective);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
