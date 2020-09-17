import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LectureRankListComponent } from './lecture-rank-list.component';

describe('LectureRankListComponent', () => {
  let component: LectureRankListComponent;
  let fixture: ComponentFixture<LectureRankListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LectureRankListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LectureRankListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
