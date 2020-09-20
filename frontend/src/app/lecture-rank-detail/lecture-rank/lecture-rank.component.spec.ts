import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureRankComponent } from './lecture-rank.component';

describe('LectureRankComponent', () => {
  let component: LectureRankComponent;
  let fixture: ComponentFixture<LectureRankComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureRankComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureRankComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
