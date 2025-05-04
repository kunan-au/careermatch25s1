// Pagination.tsx
import { FC } from 'react';
import { useSearchParams } from 'react-router-dom';
import { PAGE_SIZE } from '../../utils/constants';

interface PaginationProps {
  totalItemsCount: number;
}

const Pagination: FC<PaginationProps> = ({ totalItemsCount }) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const currentPage = !searchParams.get("page") ? 1 : Number(searchParams.get("page"));
  const pageCount = Math.ceil(totalItemsCount / PAGE_SIZE);

  function nextPage() {
    const next = currentPage === pageCount ? currentPage : currentPage + 1;
    searchParams.set("page", String(next));
    setSearchParams(searchParams);
  }

  function prevPage() {
    const prev = currentPage === 1 ? currentPage : currentPage - 1;
    searchParams.set("page", String(prev));
    setSearchParams(searchParams);
  }

  if (pageCount <= 1) return null;

  return (
    <div className="inline-flex border border-[#e4e4e4] bg-white p-4 rounded-xl">
      <ul className="flex items-center -mx-[6px]">
        <li className="px-[6px]">
          <p className="text-[#838995] text-base">
            Showing <span>{(currentPage - 1) * PAGE_SIZE + 1}</span> to{" "}
            <span>
              {currentPage * PAGE_SIZE < totalItemsCount
                ? currentPage * PAGE_SIZE
                : totalItemsCount}
            </span>{" "}
            of <span>{totalItemsCount}</span> results
          </p>
        </li>
        <li className="px-[6px]">
          <button
            onClick={prevPage}
            disabled={currentPage === 1}
            type="button"
            className="w-9 h-9 flex items-center justify-center rounded-md border border-[#EDEFF1] text-[#838995] text-base hover:bg-primary hover:border-primary hover:text-white focus:outline-none"
          >
            Prev
          </button>
        </li>
        <li className="px-[6px]">
          <button
            onClick={nextPage}
            disabled={currentPage === pageCount}
            type="button"
            className="w-9 h-9 flex items-center justify-center rounded-md border border-[#EDEFF1] text-[#838995] text-base hover:bg-primary hover:border-primary hover:text-white focus:outline-none"
          >
            Next
          </button>
        </li>
      </ul>
    </div>
  );
};

export default Pagination;
