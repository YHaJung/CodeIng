import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { QnaCardComponent } from './qna-card.component';

describe('QnaCardComponent', () => {
  let component: QnaCardComponent;
  let fixture: ComponentFixture<QnaCardComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ QnaCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QnaCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
