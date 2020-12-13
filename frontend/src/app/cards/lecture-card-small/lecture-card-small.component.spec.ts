import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { LectureCardSmallComponent } from './lecture-card-small.component';

describe('LectureCardSmallComponent', () => {
  let component: LectureCardSmallComponent;
  let fixture: ComponentFixture<LectureCardSmallComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureCardSmallComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureCardSmallComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
