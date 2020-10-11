import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReviseUserinfoComponent } from './revise-userinfo.component';

describe('ReviseUserinfoComponent', () => {
  let component: ReviseUserinfoComponent;
  let fixture: ComponentFixture<ReviseUserinfoComponent>;

  beforeEach(async(() => {
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
