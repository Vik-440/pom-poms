import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlertComponent } from './alert.component';
import { By } from '@angular/platform-browser';

describe('AlertComponent', () => {
  let component: AlertComponent;
  let fixture: ComponentFixture<AlertComponent>;
  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ AlertComponent ],
    });
    fixture = TestBed.createComponent(AlertComponent);
    component = fixture.componentInstance; // BannerComponent test instance
  });

  it('should create an instance', () => {
    expect(component).toBeTruthy();
  });

  it('should emit close', () => {
    jest.spyOn(component.closed, 'emit');
    const closeButton = fixture.debugElement.query(By.css('.close')).nativeElement;
    closeButton.click();
    expect(component.closed.emit).toHaveBeenCalled();
  })
});
