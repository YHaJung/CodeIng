import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ReviseUserinfoComponent } from './revise-userinfo.component';

describe('ReviseUserinfoComponent', () => {
  let component: ReviseUserinfoComponent;
  let fixture: ComponentFixture<ReviseUserinfoComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ReviseUserinfoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReviseUserinfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
