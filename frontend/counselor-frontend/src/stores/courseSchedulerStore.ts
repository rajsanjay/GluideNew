import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";
import type { Term, PlacedCourse, Connection, SearchFilters } from "@/types/course-scheduler";

interface CourseSchedulerState {
  // State
  terms: Term[];
  connections: Connection[];
  searchFilters: SearchFilters;
  undoStack: Term[][];
  redoStack: Term[][];
  selectedCourseId: string | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setTerms: (terms: Term[]) => void;
  addCourseToTerm: (termId: number, course: PlacedCourse) => void;
  removeCourseFromTerm: (termId: number, courseId: string) => void;
  moveCourse: (fromTermId: number, toTermId: number, courseId: string) => void;
  addConnection: (connection: Connection) => void;
  removeConnection: (connectionId: string) => void;
  setSearchFilters: (filters: Partial<SearchFilters>) => void;
  setSelectedCourse: (courseId: string | null) => void;
  undo: () => void;
  redo: () => void;
  clearSchedule: () => void;
  loadSchedule: (scheduleData: Term[]) => void;
}

export const useCourseSchedulerStore = create<CourseSchedulerState>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        terms: [
          { id: 1, courses: [], from: "", to: "" },
          { id: 2, courses: [], from: "", to: "" },
          { id: 3, courses: [], from: "", to: "" },
          { id: 4, courses: [], from: "", to: "" },
        ],
        connections: [],
        searchFilters: { query: "", department: "", credits: null },
        undoStack: [],
        redoStack: [],
        selectedCourseId: null,
        isLoading: false,
        error: null,

        // Actions
        setTerms: (terms) => {
          const current = get().terms;
          set({
            terms,
            undoStack: [...get().undoStack, current],
            redoStack: [],
          });
        },

        addCourseToTerm: (termId, course) => {
          const terms = get().terms.map((term) =>
            term.id === termId
              ? { ...term, courses: [...term.courses, course] }
              : term
          );
          get().setTerms(terms);
        },

        removeCourseFromTerm: (termId, courseId) => {
          const terms = get().terms.map((term) =>
            term.id === termId
              ? {
                  ...term,
                  courses: term.courses.filter((c) => c.id !== courseId),
                }
              : term
          );
          get().setTerms(terms);
        },

        moveCourse: (fromTermId, toTermId, courseId) => {
          const terms = get().terms;
          const fromTerm = terms.find((t) => t.id === fromTermId);
          const course = fromTerm?.courses.find((c) => c.id === courseId);

          if (!course) return;

          const newTerms = terms.map((term) => {
            if (term.id === fromTermId) {
              return {
                ...term,
                courses: term.courses.filter((c) => c.id !== courseId),
              };
            }
            if (term.id === toTermId) {
              return {
                ...term,
                courses: [...term.courses, course],
              };
            }
            return term;
          });

          get().setTerms(newTerms);
        },

        addConnection: (connection) => {
          set({ connections: [...get().connections, connection] });
        },

        removeConnection: (connectionId) => {
          set({
            connections: get().connections.filter((c) => c.id !== connectionId),
          });
        },

        setSearchFilters: (filters) => {
          set({ searchFilters: { ...get().searchFilters, ...filters } });
        },

        setSelectedCourse: (courseId) => {
          set({ selectedCourseId: courseId });
        },

        undo: () => {
          const { undoStack, terms } = get();
          if (undoStack.length === 0) return;

          const previousState = undoStack[undoStack.length - 1];
          set({
            terms: previousState,
            undoStack: undoStack.slice(0, -1),
            redoStack: [...get().redoStack, terms],
          });
        },

        redo: () => {
          const { redoStack, terms } = get();
          if (redoStack.length === 0) return;

          const nextState = redoStack[redoStack.length - 1];
          set({
            terms: nextState,
            redoStack: redoStack.slice(0, -1),
            undoStack: [...get().undoStack, terms],
          });
        },

        clearSchedule: () => {
          const emptyTerms = get().terms.map((term) => ({
            ...term,
            courses: [],
          }));
          get().setTerms(emptyTerms);
          set({ connections: [] });
        },

        loadSchedule: (scheduleData) => {
          set({
            terms: scheduleData,
            undoStack: [],
            redoStack: [],
          });
        },
      }),
      {
        name: "course-scheduler-storage",
        partialize: (state) => ({
          terms: state.terms,
          connections: state.connections,
        }),
      }
    ),
    { name: "CourseScheduler" }
  )
);
