import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MypageNavComponent } from './mypage-nav.component';

describe('MypageNavComponent', () => {
  let component: MypageNavComponent;
  let fixture: ComponentFixture<MypageNavComponent>;

  beforeEach(async(() => {
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
