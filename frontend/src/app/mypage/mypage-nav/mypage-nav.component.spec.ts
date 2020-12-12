import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { MypageNavComponent } from './mypage-nav.component';

describe('MypageNavComponent', () => {
  let component: MypageNavComponent;
  let fixture: ComponentFixture<MypageNavComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ MypageNavComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MypageNavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
