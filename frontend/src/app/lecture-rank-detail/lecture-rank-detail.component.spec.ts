import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureRankDetailComponent } from './lecture-rank-detail.component';

describe('LectureRankDetailComponent', () => {
  let component: LectureRankDetailComponent;
  let fixture: ComponentFixture<LectureRankDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureRankDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureRankDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
